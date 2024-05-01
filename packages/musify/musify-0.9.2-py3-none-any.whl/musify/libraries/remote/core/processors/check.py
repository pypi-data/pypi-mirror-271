"""
Processor operations that help a user to check whether the currently matched ID is valid for given items.

Provides the user the ability to modify associated IDs using a Remote player as an interface for
reviewing matches through temporary playlist creation.
"""
import logging
from collections import Counter
from collections.abc import Sequence, Collection, Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any

from musify import PROGRAM_NAME
from musify.core.base import MusifyItemSettable
from musify.core.enum import Fields
from musify.core.result import Result
from musify.libraries.core.collection import MusifyCollection
from musify.libraries.remote.core.api import RemoteAPI
from musify.libraries.remote.core.enum import RemoteIDType, RemoteObjectType
from musify.libraries.remote.core.factory import RemoteObjectFactory
from musify.libraries.remote.core.processors.search import RemoteItemSearcher
from musify.log import REPORT
from musify.log.logger import MusifyLogger
from musify.processors.base import InputProcessor
from musify.processors.match import ItemMatcher
from musify.utils import get_max_width, align_string

ALLOW_KARAOKE_DEFAULT = RemoteItemSearcher.search_settings[RemoteObjectType.TRACK].allow_karaoke


@dataclass(frozen=True)
class ItemCheckResult[T: MusifyItemSettable](Result):
    """Stores the results of the checking process."""
    #: Sequence of Items that had URIs switched during the check.
    switched: Sequence[T] = field(default=tuple())
    #: Sequence of Items that were marked as unavailable.
    unavailable: Sequence[T] = field(default=tuple())
    #: Sequence of Items that were skipped from the check.
    skipped: Sequence[T] = field(default=tuple())


class RemoteItemChecker(InputProcessor):
    """
    Runs operations for checking the URIs associated with a collection of items.

    When running :py:func:`check`, the object will do the following:
        * Make temporary playlists for each collection up to a ``interval`` limit of playlists.
          At which point, playlist creation pauses.
        * User can then check and modify the temporary playlists to match items to correct items or otherwise.
        * When operations resume at the user's behest, the program will search each playlist to find changes
          and attempt to match any new items to a source item.
        * If no matches are found for certain items, the program will prompt the user
          to determine how they wish to deal with these items.
        * Operation completes once user exists or all items have an associated URI.

    :param matcher: The :py:class:`ItemMatcher` to use when comparing any changes made by the user in remote playlists
        during the checking operation
    :param object_factory: The :py:class:`RemoteObjectFactory` to use when creating new remote objects.
        This must have a :py:class:`RemoteAPI` assigned for this processor to work as expected.
    :param interval: Stop creating playlists after this many playlists have been created and pause for user input.
    :param allow_karaoke: When True, items determined to be karaoke are allowed when matching switched items.
        Skip karaoke results otherwise. Karaoke items are identified using the ``karaoke_tags`` attribute.
    """

    __slots__ = (
        "interval",
        "allow_karaoke",
        "factory",
        "_playlist_name_urls",
        "_playlist_name_collection",
        "_skip",
        "_quit",
        "_remaining",
        "_switched",
        "_final_switched",
        "_final_unavailable",
        "_final_skipped",
    )

    @property
    def api(self) -> RemoteAPI:
        """The :py:class:`RemoteAPI` to call"""
        return self.factory.api

    def __init__(
            self,
            matcher: ItemMatcher,
            object_factory: RemoteObjectFactory,
            interval: int = 10,
            allow_karaoke: bool = ALLOW_KARAOKE_DEFAULT
    ):
        super().__init__()

        # noinspection PyTypeChecker
        #: The :py:class:`MusifyLogger` for this  object
        self.logger: MusifyLogger = logging.getLogger(__name__)

        #: The :py:class:`ItemMatcher` to use when comparing any changes made by the user in remote playlists
        #: during the checking operation
        self.matcher = matcher
        #: The :py:class:`RemoteObjectFactory` to use when creating new remote objects.
        self.factory = object_factory
        #: Stop creating playlists after this many playlists have been created and pause for user input
        self.interval = interval
        #: Allow karaoke items when matching on switched items
        self.allow_karaoke = allow_karaoke

        #: Map of playlist names to their URLs for created temporary playlists
        self._playlist_name_urls = {}
        #: Map of playlist names to the collection of items added for created temporary playlists
        self._playlist_name_collection = {}

        #: When true, skip the current loop and eventually safely quit check
        self._skip = False
        #: When true, safely quit check
        self._quit = False

        #: The currently remaining items that the user needs to manually check
        self._remaining: list[MusifyItemSettable] = []
        #: The list of items with switched URIs currently processed by the checker
        self._switched: list[MusifyItemSettable] = []

        #: The final list of items with switched URIs as processed by the checker
        self._final_switched: list[MusifyItemSettable] = []
        #: The final list of items marked as unavailable for this remote source
        self._final_unavailable: list[MusifyItemSettable] = []
        #: The final list of items skipped by the checker
        self._final_skipped: list[MusifyItemSettable] = []

    def _check_api(self):
        """Check if the API token has expired and refresh as necessary"""
        if not self.api.handler.test_token():  # check if token has expired
            self.logger.info_extra("\33[93mAPI token has expired, re-authorising... \33[0m")
            self.api.authorise()

    def _create_playlist(self, collection: MusifyCollection[MusifyItemSettable]) -> None:
        """Create a temporary playlist, store its URL for later unfollowing, and add all given URIs."""
        self._check_api()

        uris = [item.uri for item in collection if item.has_uri]
        if not uris:
            return

        url = self.api.create_playlist(collection.name, public=False)
        self._playlist_name_urls[collection.name] = url
        self._playlist_name_collection[collection.name] = collection

        self.api.add_to_playlist(url, items=uris, skip_dupes=False)

    def _delete_playlists(self) -> None:
        """Delete all temporary playlists stored and clear stored playlists and collections"""
        self._check_api()

        self.logger.info_extra(f"\33[93mDeleting {len(self._playlist_name_urls)} temporary playlists... \33[0m")
        for url in self._playlist_name_urls.values():  # delete playlists
            self.api.delete_playlist(url)

        self._playlist_name_urls.clear()
        self._playlist_name_collection.clear()

    def __call__(self, *args, **kwargs) -> ItemCheckResult | None:
        return self.check(*args, **kwargs)

    def check[T: MusifyItemSettable](self, collections: Collection[MusifyCollection[T]]) -> ItemCheckResult[T] | None:
        """
        Run the checker for the given ``collections``.

        :param collections: A list of collections to check.
        :return: A :py:class:`ItemCheckResult` object containing the remapped items created during the check.
            Return None when the user opted to quit (not skip) the checker before completion.
        """
        if len(collections) == 0 or all(not collection.items for collection in collections):
            self.logger.debug("\33[93mNo items to check. \33[0m")
            return

        self.logger.debug("Checking items: START")
        self.logger.info(
            f"\33[1;95m ->\33[1;97m Checking items by creating temporary {self.api.source} playlists "
            f"for the current user: {self.api.user_name} \33[0m"
        )

        total = len(collections)
        pages_total = (total // self.interval) + (total % self.interval > 0)
        bar = self.logger.get_progress_bar(total=total, desc="Creating temp playlists", unit="playlists")

        self._skip = False
        self._quit = False

        collections_iter = (collection for collection in collections)
        for page in range(1, pages_total + 1):
            try:
                for count, collection in enumerate(collections_iter, 1):
                    self._create_playlist(collection=collection)
                    bar.update(1)
                    if count >= self.interval:
                        break

                self._pause(page=page, total=pages_total)
                if not self._quit:  # still run if skip is True
                    self._check_uri()
            except KeyboardInterrupt:
                self.logger.error("User triggered exit with KeyboardInterrupt")
                self._quit = True
            finally:
                self._delete_playlists()

            if self._quit or self._skip:  # quit check
                break

        bar.close()
        result = self._finalise() if not self._quit else None
        self.logger.debug("Checking items: DONE\n")
        return result

    def _finalise(self) -> ItemCheckResult:
        """Log results and prepare the :py:class:`ItemCheckResult` object"""
        self.logger.print()
        self.logger.report(
            f"\33[1;96mCHECK TOTALS \33[0m| "
            f"\33[94m{len(self._final_switched):>5} switched  \33[0m| "
            f"\33[91m{len(self._final_unavailable):>5} unavailable \33[0m| "
            f"\33[93m{len(self._final_skipped):>5} skipped \33[0m"
        )
        self.logger.print(REPORT)

        result = ItemCheckResult(
            switched=self._final_switched, unavailable=self._final_unavailable, skipped=self._final_skipped
        )

        self._skip = True
        self._remaining.clear()
        self._switched.clear()
        self._final_switched = []
        self._final_unavailable = []
        self._final_skipped = []

        return result

    ###########################################################################
    ## Pause to check items in current temp playlists
    ###########################################################################
    def _pause(self, page: int, total: int) -> None:
        """
        Initial pause after the ``interval`` limit of playlists have been created.

        :param page: The current page number i.e. the current number of pauses that have happened so far.
        :param total: The total number of pages (pauses) that will occur in this run.
        """
        header = [
            f"\t\33[1;94mTemporary playlists created on {self.api.source}.",
            f"You may now check the songs in each playlist on {self.api.source}. \33[0m"
        ]
        options = {
            "<Name of playlist>":
                "Print position, item name, URI, and URL from given link of items as originally added to temp playlist",
            f"<{self.api.source} URL/URI>":
                "Print position, item name, URI, and URL from given link (useful to check current status of playlist)",
            "<Return/Enter>":
                "Once you have checked all playlist's items, continue on and check for any switches by the user",
            "s": "Check for changes on current playlists, but skip any remaining checks",
            "q": "Delete current temporary playlists and quit check",
            "h": "Show this dialogue again",
        }

        current_input = "START"
        help_text = self._format_help_text(options=options, header=header)

        print("\n" + help_text)
        while current_input != '':  # while user has not hit return only
            current_input = self._get_user_input(f"Enter ({page}/{total})")
            pl_name = next((
                name for name in self._playlist_name_collection
                if current_input and current_input.casefold() in name.casefold()
            ), None)

            if current_input.casefold() == "h":  # print help text
                print("\n" + help_text)

            elif current_input.casefold() == 's' or current_input.casefold() == 'q':  # quit/skip
                self._quit = current_input.casefold() == 'q' or self._quit
                self._skip = current_input.casefold() == 's' or self._skip
                break

            elif pl_name:  # print originally added items
                items = [item for item in self._playlist_name_collection[pl_name] if item.has_uri]
                max_width = get_max_width(items)

                print(f"\n\t\33[96mShowing items originally added to \33[94m{pl_name}\33[0m:\n")
                for i, item in enumerate(items, 1):
                    length = getattr(item, "length", 0)
                    self.api.print_item(
                        i=i, name=item.name, uri=item.uri, length=length, total=len(items), max_width=max_width
                    )
                print()

            elif self.api.wrangler.validate_id_type(current_input):  # print URL/URI/ID result
                self._check_api()
                self.api.print_collection(current_input)

            elif current_input != "":
                self.logger.warning("Input not recognised.")

    ###########################################################################
    ## Match items user has added or removed
    ###########################################################################
    def _check_uri(self) -> None:
        """Run operations to check that URIs are assigned to all the items in the current list of collections."""
        skip_hold = self._skip
        self._skip = False
        for name, collection in self._playlist_name_collection.items():
            self.matcher.log_messages([name, f"{len(collection):>6} total items"], pad='>')

            while True:
                self._match_to_remote(name=name)
                self._match_to_input(name=name)
                if not self._remaining:
                    break

            unavailable = tuple(item for item in collection if item.has_uri is False)
            skipped = tuple(item for item in collection if item.has_uri is None)

            self.matcher.log_messages([name, f"{len(self._switched):>6} items switched"], pad='<')
            self.matcher.log_messages([name, f"{len(unavailable):>6} items unavailable"])
            self.matcher.log_messages([name, f"{len(skipped):>6} items skipped"])

            self._final_switched += self._switched
            self._final_unavailable += unavailable
            self._final_skipped += skipped
            self._switched.clear()

            if self._quit or self._skip:
                break

        self._skip = skip_hold

    def _match_to_remote(self, name: str) -> None:
        """
        Check the current temporary playlist given by ``name`` and attempt to match the source list of items
        to any modifications the user has made.
        """
        self._check_api()

        self.logger.info(
            "\33[1;95m ->\33[1;97m Checking for changes to items in "
            f"{self.api.source} playlist: \33[94m{name}\33[0m..."
        )

        source = self._playlist_name_collection[name]
        source_valid = [item for item in source if item.has_uri]

        remote_response = self.api.get_items(self._playlist_name_urls[name], extend=True, use_cache=False)[0]
        remote = self.factory.playlist(response=remote_response).items
        remote_valid = [item for item in remote if item.has_uri]

        added = [item for item in remote_valid if item not in source]
        removed = [item for item in source_valid if item not in remote] if not self._remaining else []
        missing = self._remaining or [item for item in source if item.has_uri is None]

        if len(added) + len(removed) + len(missing) == 0:
            if len(source_valid) == len(remote_valid):
                self.matcher.log_messages([name, "Playlist unchanged and no missing URIs, skipping match"])
                return

            # if item collection originally contained duplicate URIS and one or more of the duplicates were removed,
            # find missing items by looking for changes in counts
            remote_counts = Counter(item.uri for item in remote_valid)
            for uri, count in Counter(item.uri for item in source_valid).items():
                if remote_counts.get(uri) != count:
                    missing.extend([item for item in source_valid if item.uri == uri])

        self.matcher.log_messages([name, f"{len(added):>6} items added"])
        self.matcher.log_messages([name, f"{len(removed):>6} items removed"])
        self.matcher.log_messages([name, f"{len(missing):>6} items in source missing URI"])
        self.matcher.log_messages([name, f"{len(source_valid) - len(remote_valid):>6} total difference"])

        remaining = removed + missing
        count_start = len(remaining)
        with ThreadPoolExecutor(thread_name_prefix="checker") as executor:
            tasks: Iterator[tuple[MusifyItemSettable, MusifyItemSettable | None]] = executor.map(
                lambda item: (
                    item, self.matcher(item, results=added, match_on=[Fields.TITLE], allow_karaoke=self.allow_karaoke)
                ),
                remaining if added else ()
            )

        for item, match in tasks:
            if not match:
                continue

            item.uri = match.uri

            added.remove(match)
            removed.remove(item) if item in removed else missing.remove(item)
            self._switched.append(match)

        self._remaining = removed + missing
        count_final = len(self._remaining)
        self.matcher.log_messages([name, f"{count_start - count_final:>6} items switched"])
        self.matcher.log_messages([name, f"{count_final:>6} items still not found"])

    def _match_to_input(self, name: str) -> None:
        """
        Get the user's input for any items in the ``remaining`` list that are still missing URIs.
        Provide a ``name`` to use for logging only.
        """
        if not self._remaining:
            return

        header = [f"\t\33[1;94m{name}:\33[91m The following items were removed and/or matches were not found. \33[0m"]
        options = {
            "u": f"Mark item as 'Unavailable on {self.api.source}'",
            "n": f"Leave item with no URI. ({PROGRAM_NAME} will still attempt to find this item at the next run)",
            "a": "Add in addition to 'u' or 'n' options to apply this setting to all items in this playlist",
            "r": "Recheck playlist for all items in the collection",
            "p": "Print the local path of the current item if available",
            "s": "Skip checking process for all current playlists",
            "q": "Skip checking process for all current playlists and quit check",
            "h": "Show this dialogue again",
        }

        current_input = ""
        help_text = self._format_help_text(options=options, header=header)
        help_text += "OR enter a custom URI/URL/ID for this item\n"

        self.matcher.log_messages([name, f"Getting user input for {len(self._remaining)} items"])
        max_width = get_max_width({item.name for item in self._remaining})

        print("\n" + help_text)
        for item in self._remaining.copy():
            while current_input is not None and item in self._remaining:  # while item not matched or skipped
                self.matcher.log_messages([name, f"{len(self._remaining):>6} remaining items"])
                if 'a' not in current_input:
                    current_input = self._get_user_input(align_string(item.name, max_width=max_width))

                if current_input.casefold() == 'h':  # print help
                    print("\n" + help_text)
                else:
                    current_input = self._match_item_to_input(name=name, item=item, current_input=current_input)

            if current_input is None or not self._remaining:
                break

    def _match_item_to_input(self, name: str, item: MusifyItemSettable, current_input: str) -> str | None:
        if current_input.casefold() == 's' or current_input.casefold() == 'q':  # quit/skip
            self.matcher.log_messages([name, "Skipping all loops"], pad="<")
            self._quit = current_input.casefold() == 'q' or self._quit
            self._skip = current_input.casefold() == 's' or self._skip
            self._remaining.clear()
            return

        elif current_input.casefold().replace('a', '') == 'u':  # mark item as unavailable
            self.matcher.log_messages([name, "Marking as unavailable"], pad="<")
            item.uri = self.api.wrangler.unavailable_uri_dummy
            self._remaining.remove(item)

        elif current_input.casefold().replace('a', '') == 'n':  # leave item without URI and unprocessed
            self.matcher.log_messages([name, "Skipping"], pad="<")
            item.uri = None
            self._remaining.remove(item)

        elif current_input.casefold() == 'r':  # return to former 'while' loop
            self.matcher.log_messages([name, "Refreshing playlist metadata and restarting loop"])
            return

        elif current_input.casefold() == 'p' and hasattr(item, "path"):  # print item path
            print(f"\33[96m{item.path}\33[0m")

        elif self.api.wrangler.validate_id_type(current_input):  # update URI and add item to switched list
            uri = self.api.wrangler.convert(
                current_input, kind=RemoteObjectType.TRACK, type_out=RemoteIDType.URI
            )

            self.matcher.log_messages([name, f"Updating URI: {item.uri} -> {uri}"], pad="<")
            item.uri = uri

            self._switched.append(item)
            self._remaining.remove(item)
            current_input = ""

        elif current_input:  # invalid input
            self.logger.warning("Input not recognised.")
            current_input = ""

        return current_input

    def as_dict(self) -> dict[str, Any]:
        return {
            "matcher": self.matcher,
            "remote_source": self.factory.api.source,
            "interval": self.interval,
            "allow_karaoke": self.allow_karaoke,
        }
