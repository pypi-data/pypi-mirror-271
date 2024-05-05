"""
This class contains the code for extracting the data provided by InnerTube.
"""
import logging

from datetime import time, date

from typing import (
    Optional,
    Tuple,
    Union,
    List,
    Dict,
    Callable,
    Any
)

from innertube_de.endpoints import (
    ContinuationEndpoint,
    Endpoint,
    BrowseEndpoint,
    YouTubeBrowseEndpoint,
    WatchEndpoint,
    UrlEndpoint,
    SearchEndpoint
)

from innertube_de.containers import (
    CardShelf,
    Shelf,
    Container
)

from innertube_de.items import (
    Item,
    RadioItem,
    YouTubeMusicVideoItem,
    YouTubeVideoItem,
    YouTubeMusicPlaylistItem,
    YouTubePlaylistItem,
    ChannelItem,
    AlbumItem,
    ArtistItem,
    SongItem,
    SingleItem,
    EPItem,
    PodcastItem,
    ProfileItem,
    EpisodeItem,
)

from innertube_de.stream import StreamData
from innertube_de.types import (
    EndpointType,
    ContinuationStrucType,
    ItemStructType,
    ShelfStructType,
    ResultStructType,
    ItemType,
    TextDivisorType
)

from innertube_de.utils import (
    get_item_type,
    to_int,
    return_on_input_none,
    get,
    clc_length,
    clc_publication_date,
    clc_int,
    clc_views
)

from innertube_de.errors import (
    ErrorWrapper,
    AccessError,
    ExtractionError
)


log = logging.getLogger(__name__)


def extract(
        data: Dict, 
        *,
        log_errors: bool = True, 
        stack_info: bool = True, 
        exc_info: bool = True, 
        enable_exceptions: bool = True,
        include_all_urls: bool = True
) -> Container:
    innertube_de = InnerTubeDE(
        log_errors=log_errors, 
        stack_info=stack_info, 
        exc_info=exc_info, 
        enable_exceptions=enable_exceptions,
        include_all_urls=include_all_urls
    )
    return innertube_de.extract(data)


class InnerTubeDE:
    """
    Class for instantiating objects for extracting data provided by InnerTube.
    Works with the search, next, browse functions of an InnerTube client.
    See https://github.com/tombulled/innertube as an example of an InnerTube client.
    """
    def __init__(
            self,
            *,
            log_errors: bool = True,
            stack_info: bool = True,
            exc_info: bool = True,
            enable_exceptions: bool = True,
            include_all_urls: bool = False
    ) -> None:
        """
        Initialize an Extractor object with specified parameters.
        @param log_errors: When set to True, if an anomaly occurs,
        information about the anomaly is printed in the log.
        @param enable_exceptions: When set to True, when an anomaly
        occurs, an ExtractorError exception is thrown and the extraction
        process terminates.
        """
        self.log_errors = log_errors
        self.stack_info = stack_info
        self.exc_info = exc_info
        self.enable_exceptions = enable_exceptions
        self.include_all_urls = include_all_urls

    @staticmethod
    def _handle_main_function(func: Callable) -> Callable:
        def inner(self, data: Dict) -> Union[Container, List[StreamData]]:
            if not isinstance(data, Dict):
                raise TypeError(f"Invalid input type: {type(data)}. Expected input type: Dict")
            try:
                result = func(self, data)
            except Exception:
                raise ExtractionError(
                    "An error occurred during the data extraction process. "
                    "Please open an issue at https://github.com/g3nsy/innertube-de/issues"
                    " and reports this log message."
                )
            else:
                return result
        return inner

    @_handle_main_function
    def extract(self, data: Dict) -> Container:
        """
        Main method for extracting the data provided by InnerTube.
        @param data: The data provided by an InnerTube client.
        @raise ExtractorError: If an anomaly occurs during the extraction
        process and the 'enable_exceptions' field of the invoking object
        is set to the value True.
        """
        # Extracting the item in the header
        header_data = self._get(data, "header", opt=True)
        if header_data is None:
            header = None
        else:
            header = self._extract_item(header_data, opt=True)

        data_contents = self._extract_contents(data)
        container = Container(header=header, contents=None)
        # Sometimes the data provided by InnerTube does not
        # contain any data of interest.
        if data_contents is None:
            return container

        # Extraction of the 'shelves', i.e. the sub-containers
        # that contain the multimedia objects
        shelves: List[Shelf] = []
        for entry in data_contents:
            shelf = self._extract_shelf(entry)
            if shelf is not None:
                shelves.append(shelf)
        container.contents = shelves

        return container

    @staticmethod
    def _handle_exception(func: Callable) -> Callable:
        """
        Decorator that allows you to manage the occurrence of exceptions during
        the execution of methods that access and/or manipulate the data provided
        by InnerTube.
        @param func: The function to decorate.
        @return: The decorated function.
        """
        def inner(*args, opt: bool = False, **kwargs) -> Optional[Any]:
            if not isinstance(args[0], InnerTubeDE):
                raise RuntimeError(f"Invalid input type: {type(args[0])}. Expected input type: InnerTubeDE")
            try:
                return func(*args, **kwargs)
            except Exception as error:
                if opt is False:
                    # _ErrorWrapper prevent the following from occurring:
                    # [2024-04-17 19:17:46,845 ERROR in extractor]: Executing function _clc_int ...
                    # [2024-04-17 19:17:46,845 ERROR in extractor]: Executing function _extract_item ...
                    # [2024-04-17 19:17:46,845 ERROR in extractor]: Executing function _extract_shelf ...
                    if args[0].log_errors is True and not isinstance(error, ErrorWrapper):
                        log.error(
                            f"Executing function {func.__name__} caused an exception: "
                            f"{error.__class__.__name__}"
                            f": {error.args[0]}" if error.args[0] is not None else "",
                            stack_info=False if args[0].enable_exceptions is True else args[0].stack_info,
                            exc_info=False if args[0].enable_exceptions is True else args[0].exc_info
                        )

                    if args[0].enable_exceptions is True:
                        if isinstance(error, ErrorWrapper):
                            raise error
                        else:
                            raise ErrorWrapper(error)
                return None
        return inner

    @_handle_exception
    def _extract_contents(self, data: Dict) -> Optional[List[Dict]]:
        """
        Method for extracting contents, i.e. the list of 'shelves'
        containing multimedia objects.
        @param data: The data provided by an InnerTube client.
        @return: A list of dictionaries, containing 'shelf' data.
        Returns None if the specified input contains no content.
        """
        # YouTube Music / YouTube
        if ContinuationStrucType.CONTINUATION.value in data:
            ds = self._get(data, ContinuationStrucType.CONTINUATION.value)

            if ContinuationStrucType.SECTION_LIST.value in ds:
                ds = self._get(ds, ContinuationStrucType.SECTION_LIST.value, "contents")

                # YouTube - browse
                if ShelfStructType.ITEM_SECTION.value in self._get(ds, 0):
                    shelves: List[Dict] = []
                    for entry in ds:
                        tmp = self._get(entry, ShelfStructType.ITEM_SECTION.value, "contents", 0)
                        if ItemStructType.CHANNEL_VIDEO_PLAYER.value in tmp:
                            shelves.append({ShelfStructType.CHANNEL_SHELF.value: {"contents": [tmp]}})
                        else:
                            shelves.append(tmp)
                    return shelves

                # YouTube Music - browse
                else:
                    return ds

            # YouTube Music
            elif ContinuationStrucType.MUSIC_PLAYLIST_SHELF.value in ds:
                return [{
                    ShelfStructType.MUSIC_SHELF.value: self._get(
                        ds, ContinuationStrucType.MUSIC_PLAYLIST_SHELF.value
                    )
                }]

            # YouTube Music 
            elif ContinuationStrucType.MUSIC_SHELF.value in ds:
                return [{
                    ShelfStructType.MUSIC_SHELF.value: self._get(
                        ds, ContinuationStrucType.MUSIC_SHELF.value
                    )
                }]

            # YouTube - browse
            elif ShelfStructType.PLAYLIST_VIDEO_LIST_CONTINUATION.value in ds:
                return [ds]

            else:
                raise AccessError(data=ds)

        elif ResultStructType.ON_RESPONSE_RECEIVED_ENDPOINTS.value in data:
            tmp = self._get(
                data, ResultStructType.ON_RESPONSE_RECEIVED_ENDPOINTS.value, 0, 
                "appendContinuationItemsAction", "continuationItems", opt=True
            )

            if tmp is not None:
                return tmp

        data = self._get(data, "contents", opt=True)
        if data is None:
            return None

        if ResultStructType.TWO_COLUMN_BROWSE_RESULT.value in data:
            ds = self._get(data, ResultStructType.TWO_COLUMN_BROWSE_RESULT.value)

            # YouTube Music
            if "secondaryContents" in ds:
                return self._get(ds, "secondaryContents", "sectionListRenderer", "contents")

            # YouTube
            elif "tabs" in ds:
                tmp = self._get(
                    ds, "tabs", 0, "tabRenderer", "content", "sectionListRenderer", "contents"
                )
                shelves: List[Dict] = []
                for entry in tmp:
                    if ItemStructType.CONTINUATION_ITEM.value in entry:
                        continue
                    tmp1 = self._get(entry, ShelfStructType.ITEM_SECTION.value, "contents", 0)
                    if ItemStructType.CHANNEL_VIDEO_PLAYER.value in tmp1:
                        shelves.append({ShelfStructType.CHANNEL_SHELF.value: {"contents": [tmp1]}})
                    else:
                        shelves.append(tmp1)
                return shelves
            else:
                raise AccessError(data=ds)

        # YouTube Music
        elif ResultStructType.SINGLE_COLUMN_BROWSE_RESULTS.value in data:
            tmp1 = self._get(
                data, ResultStructType.SINGLE_COLUMN_BROWSE_RESULTS.value, "tabs", 0,
                "tabRenderer", "content", "sectionListRenderer", opt=True
            )

            if tmp1 is not None:
                tmp2 = self._get(tmp1, "contents", 0, opt=True)
                if tmp2 is not None:
                    if ShelfStructType.GRID.value in tmp2:
                        return self._get(tmp1, "contents")
                    elif ShelfStructType.MUSIC_PLAYLIST_SHELF.value in tmp2:
                        return [tmp2]
                    elif ShelfStructType.MUSIC_CAROUSEL_SHELF.value in tmp2:
                        return self._get(tmp1, "contents")
                    elif ShelfStructType.MUSIC_SHELF.value in tmp2:
                        return self._get(tmp1, "contents")
                    else:
                        raise AccessError(data=tmp2)
                else:
                    return None
            else:
                return None

        # YouTube Music
        elif ResultStructType.TABBED_SEARCH_RESULTS.value in data:
            return self._get(
                data, ResultStructType.TABBED_SEARCH_RESULTS.value, "tabs", 0, "tabRenderer", 
                "content", "sectionListRenderer", "contents"
            )

        # YouTube Music
        elif ResultStructType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT.value in data:
            tmp = self._get(
                data, ResultStructType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT.value, "tabbedRenderer",
                "watchNextTabbedResultsRenderer", "tabs", 0, "tabRenderer", "content",
                "musicQueueRenderer", "content", ShelfStructType.PLAYLIST_PANEL.value, opt=True
            )
            if tmp is not None:
                return [{ShelfStructType.PLAYLIST_PANEL.value: tmp}]

        # YouTube - search
        elif ResultStructType.TWO_COLUMN_SEARCH_RESULTS.value in data:
            contents = self._get(
                data, ResultStructType.TWO_COLUMN_SEARCH_RESULTS.value, "primaryContents",
                "sectionListRenderer", "contents", 0, "itemSectionRenderer", "contents"
            )

            results: List[Dict] = []
            shelf_contents: List[Dict] = []
            for entry in contents:
                key = list(entry.keys())[0]
                if ItemStructType.has_value(key):
                    shelf_contents.append(entry)
                elif ShelfStructType.has_value(key):
                    results.append(entry)
                    if len(shelf_contents) != 0:
                        results.append({ShelfStructType.CHANNEL_SHELF.value: {"contents": shelf_contents}})
                        shelf_contents.clear()
                else:
                    raise AccessError(data=entry, prefix=f"Key used: {key}. ")
            
            if len(shelf_contents) != 0:
                results.append({ShelfStructType.CHANNEL_SHELF.value: {"contents": shelf_contents}})

            secondary_contents = self._get(
                data,  ResultStructType.TWO_COLUMN_SEARCH_RESULTS.value, "secondaryContents",
                "secondarySearchContainerRenderer", "contents", 0, "universalWatchCardRenderer",
                "sections", opt=True
            )

            if secondary_contents is not None:
                for entry in secondary_contents:
                    results.append(self._get(entry, "watchCardSectionSequenceRenderer", "lists", 0))

            return results

        # YouTube - next
        elif ResultStructType.TWO_COLUMN_WATCH_NEXT_RESULTS.value in data:
            primary_content = self._get(
                data, ResultStructType.TWO_COLUMN_WATCH_NEXT_RESULTS.value, "results", "results", "contents"
            )

            custom_shelf = {
                ShelfStructType.NEXT_PRIMARY_SHELF.value: [{
                    ItemStructType.NEXT_PRIMARY_VIDEO.value: {
                        ItemType.YOUTUBE_VIDEO.value: self._get(
                            primary_content, 0, "videoPrimaryInfoRenderer"
                        ),
                        ItemType.CHANNEL.value: self._get(
                            primary_content, 1, "videoSecondaryInfoRenderer"
                        )
                    }
                }]
            }

            return [
                self._get(data, ResultStructType.TWO_COLUMN_WATCH_NEXT_RESULTS.value, "secondaryResults"),
                custom_shelf
            ]

        else:
            raise AccessError(data=data)

    @_handle_exception
    def _extract_shelf(self, entry: Dict) -> Optional[Shelf]:
        """
        Method for extracting the shelf from the specified dictionary.
        @param entry: Portion of the data provided by InnerTube containing
        the data of a shelf.
        @return: A Shelf object otherwise None if no registered shelf
        structure was detected in the provided dictionary.
        """
        item_type = None
        # YouTube Music
        if ShelfStructType.MUSIC_SHELF.value in entry:
            ds = self._get(entry, ShelfStructType.MUSIC_SHELF.value)
            name = self._get(ds, "title", "runs", 0, "text", opt=True)
            contents = self._get(ds, "contents")
            endpoint = self._extract_endpoint(self._get(ds, "bottomEndpoint", opt=True))
            shelf = Shelf(name=name, endpoint=endpoint)
            item_type = get_item_type(name)

        elif ShelfStructType.MUSIC_PLAYLIST_SHELF.value in entry:
            ds = self._get(entry, ShelfStructType.MUSIC_PLAYLIST_SHELF.value)
            contents = self._get(ds, "contents")
            shelf = Shelf()

        # YouTube Music
        elif ShelfStructType.MUSIC_CAROUSEL_SHELF.value in entry:
            ds = self._get(entry, ShelfStructType.MUSIC_CAROUSEL_SHELF.value)
            contents = self._get(ds, "contents")
            name = self._get(
                ds, "header", "musicCarouselShelfBasicHeaderRenderer", "title", "runs", 0, "text"
            )
            endpoint = self._extract_endpoint(
                self._get(
                    ds, "header", "musicCarouselShelfBasicHeaderRenderer", "title", 
                    "runs", 0, "navigationEndpoint", opt=True
                )
            )
            shelf = Shelf(name=name, endpoint=endpoint)
            item_type = get_item_type(name)

        # YouTube Music
        elif ShelfStructType.MUSIC_CARD_SHELF.value in entry:
            item = self._extract_item(entry)
            shelf = CardShelf(item=item)
            contents = self._get(entry, ShelfStructType.MUSIC_CARD_SHELF.value, "contents", opt=True)

        # YouTube Music
        elif ShelfStructType.PLAYLIST_PANEL.value in entry:
            ds = self._get(entry, ShelfStructType.PLAYLIST_PANEL.value)
            name = self._get(ds, "title", opt=True)
            contents = self._get(ds, "contents")
            shelf = Shelf(name=name)
            item_type = get_item_type(name)

        # YouTube Music
        elif ShelfStructType.GRID.value in entry:
            shelf = Shelf()
            contents = self._get(entry, ShelfStructType.GRID.value, "items")

        # YouTube
        elif ShelfStructType.NEXT_PRIMARY_SHELF.value in entry:
            shelf = Shelf()
            contents = self._get(entry, ShelfStructType.NEXT_PRIMARY_SHELF.value)

        # YouTube
        elif ShelfStructType.SHELF.value in entry:
            ds = self._get(entry, ShelfStructType.SHELF.value)
            name = self._get(ds, "title", "runs", 0, "text", opt=True)
            if name is None:
                name = self._get(ds, "title", "simpleText")
            endpoint = self._extract_endpoint(self._get(ds, "endpoint", opt=True), opt=True)
            if endpoint is None:
                endpoint = self._extract_endpoint(
                    self._get(
                        ds, "endpoint", "showEngagementPanelEndpoint", "engagementPanel",
                        "engagementPanelSectionListRenderer", "content", "sectionListRenderer",
                        "contents", 0, "itemSectionRenderer", "contents", 0, "continuationItemRenderer",
                        opt=True
                    )
                )
            contents = self._get(ds, "content", "horizontalListRenderer", "items", opt=True)
            if contents is None:
                contents = self._get(ds, "content", "verticalListRenderer", "items")
            shelf = Shelf(name=name, endpoint=endpoint)
            item_type = get_item_type(name)

        # YouTube
        elif ShelfStructType.SECONDARY_RESULTS.value in entry:
            contents = self._get(entry, ShelfStructType.SECONDARY_RESULTS.value, "results")
            shelf = Shelf()

        # YouTube
        elif ShelfStructType.PLAYLIST_VIDEO_LIST_CONTINUATION.value in entry:
            contents = self._get(entry, ShelfStructType.PLAYLIST_VIDEO_LIST_CONTINUATION.value, "contents")
            shelf = Shelf()

        # YouTube
        elif ShelfStructType.PLAYLIST_VIDEO_LIST.value in entry:
            contents = self._get(entry, ShelfStructType.PLAYLIST_VIDEO_LIST.value, "contents")
            shelf = Shelf()

        # YouTube
        elif ShelfStructType.CHANNEL_SHELF.value in entry:
            contents = self._get(entry, ShelfStructType.CHANNEL_SHELF.value, "contents")
            shelf = Shelf()

        elif ShelfStructType.REEL_SHELF.value in entry:
            ds = self._get(entry, ShelfStructType.REEL_SHELF.value)
            name = self._get(ds, "title", "runs", 0, "text", opt=True)
            if name is None:
                name = self._get(ds, "title", "simpleText")
            contents = self._get(ds, "items")
            shelf = Shelf(name=name)

        elif ShelfStructType.HORIZONTAL_CARD_LIST_RENDERER.value in entry:
            ds = self._get(entry, ShelfStructType.HORIZONTAL_CARD_LIST_RENDERER.value)
            name = self._get(ds, "header", "titleAndButtonListHeaderRenderer", "title", "simpleText")
            contents = self._get(ds, "cards")
            shelf = Shelf(name=name)

        elif ShelfStructType.VERTICAL_WATCH_CARD_LIST.value in entry:
            ds = self._get(entry, ShelfStructType.VERTICAL_WATCH_CARD_LIST.value)
            contents = self._get(ds, "items")
            shelf = Shelf()

        # ignored
        elif (
            ShelfStructType.ITEM_SECTION.value in entry
            or ShelfStructType.MUSIC_DESCRIPTION_SHELF.value in entry
            or ShelfStructType.SHOWING_RESULTS_FOR.value in entry
        ):
            return None

        else:
            raise AccessError(data=entry)

        if contents is not None:
            for entry_item in contents:
                item = self._extract_item(entry_item, item_type)
                if item is not None:
                    shelf.append(item)
        return shelf

    @_handle_exception
    def _extract_item(self, entry_item: Dict, item_type: Optional[ItemType] = None) -> Optional[Item]:
        """
        Method for extracting media content from the specified dictionary.
        @param entry_item: Portion of data provided by InnerTube containing
        details relating to multimedia content.
        @param item_type: Object that allows you to determine the type of
        the object to be instantiated without having to search for this data
        in the specified dictionary (it is not always possible to determine
        the type of item). This parameter, if present, indicates that the
        object belongs to a shelf whose name explains the type of objects it contains.
        @return: An Item object or None if no registered item structure
        was detected in the provided dictionary.
        """
        # YouTube Music
        if ShelfStructType.MUSIC_CARD_SHELF.value in entry_item:
            ds = self._get(entry_item, ShelfStructType.MUSIC_CARD_SHELF.value)
            item_type = get_item_type(self._get(ds, "subtitle", "runs", 0, "text"))
            name = self._get(ds, "title", "runs", 0, "text")
            endpoint = self._extract_endpoint(self._get(ds, "title", "runs", 0, "navigationEndpoint"))
            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails")
            )

            match item_type:
                case ItemType.ALBUM:
                    item = AlbumItem(name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls)

                case ItemType.ARTIST:
                    subscribers = self._clc_int(self._get(ds, "subtitle", "runs", -1, "text"))
                    item = ArtistItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, subscribers=subscribers
                    )

                case ItemType.YOUTUBE_MUSIC_VIDEO:
                    views = self._clc_int(self._get(ds, "subtitle", "runs", -3, "text"))
                    length = self._clc_length(self._get(ds, "subtitle", "runs", -1, "text"))
                    item = YouTubeMusicVideoItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, views=views, length=length
                    )

                case ItemType.EP:
                    item = EPItem(name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls)

                case ItemType.SONG:
                    length = self._clc_length(self._get(ds, "subtitle", "runs", -1, "text"))
                    album_name = self._get(ds, "subtitle", "runs", -3, "text")
                    album_endpoint = self._extract_endpoint(
                        self._get(ds, "subtitle", "runs", -3, "navigationEndpoint")
                    )

                    album_item = AlbumItem(
                        name=album_name, thumbnail_urls=thumbnail_urls, endpoint=album_endpoint
                    )

                    item = SongItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, 
                        length=length, album_item=album_item
                    )

                case ItemType.EPISODE:
                    publication_date = self._clc_publication_date(self._get(ds, "subtitle", "runs", 2))
                    item = EpisodeItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, 
                        publication_date=publication_date
                    )

                case _:
                    item = Item(name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls)

        # YouTube Music
        elif ItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value in entry_item:
            ds = self._get(entry_item, ItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value)
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint", opt=True))
            if endpoint is None:
                endpoint = self._extract_endpoint(
                    self._get(
                        ds, "flexColumns", 0, "musicResponsiveListItemFlexColumnRenderer",
                        "text", "runs", -1, "navigationEndpoint"
                    )
                )
            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails", opt=True)
            )
            name = self._get(
                ds, "flexColumns", 0, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", 0, "text"
            )
            if item_type is None:
                item_type = get_item_type(
                    self._get(
                        ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", 
                        "text", "runs", 0, "text", opt=True
                    )
                )
                if item_type is None:
                    item_type = ItemType.SONG

            match item_type:
                case ItemType.ARTIST:
                    subscribers = self._clc_int(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                            "text", "runs", -1, "text", opt=True
                        ), 
                        opt=True
                    )
                    item = ArtistItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, subscribers=subscribers
                    )

                case ItemType.ALBUM:
                    release_year = to_int(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                            "text", "runs", -1, "text"
                        )
                    )
                    item = AlbumItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls,
                        release_year=release_year, artist_items=None
                    )

                case ItemType.YOUTUBE_MUSIC_VIDEO:
                    length = self._clc_length(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text",
                            "runs", -1, "text"
                        )
                    )

                    views = self._clc_int(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                            "text", "runs", -3, "text", opt=True
                        )
                    )
                    item = YouTubeMusicVideoItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, length=length, views=views
                    )

                case ItemType.YOUTUBE_MUSIC_PLAYLIST:
                    tracks_num = to_int(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text",
                            "runs", -1, "text", opt=True
                        )
                    )

                    views = self._clc_int(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text",
                            "runs", -1, "text", opt=True
                        ),
                        opt=True
                    )

                    item = YouTubeMusicPlaylistItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, 
                        tracks_num=tracks_num, views=views
                    )

                case ItemType.SINGLE:
                    release_year = to_int(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text",
                            "runs", -1, "text", opt=True
                        )
                    )
                    item = SingleItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, release_year=release_year
                    )

                case ItemType.SONG:
                    length = self._clc_length(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", 
                            "text", "runs", -1, "text", opt=True
                        ),
                        opt=True
                    )
                    if length is None:
                        length = self._clc_length(
                            self._get(
                                ds, "fixedColumns", 0, "musicResponsiveListItemFixedColumnRenderer",
                                "text", "runs", 0, "text", opt=True
                            )
                        )

                    attempt1 = self._clc_int(
                        self._get(
                            ds, "flexColumns", -1, "musicResponsiveListItemFlexColumnRenderer",
                            "text", "runs", -1, "text", opt=True
                        ),
                        opt=True
                    )
                    if attempt1 is None:
                        attempt2 = self._clc_int(
                            self._get(
                                ds, "flexColumns", -2, "musicResponsiveListItemFlexColumnRenderer",
                                "text", "runs", -1, "text", opt=True
                            ),
                            opt=True
                        )
                        reproductions = attempt2
                    else:
                        reproductions = attempt1

                    item = SongItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls,
                        length=length, reproductions=reproductions, album_item=None
                    )

                case ItemType.EPISODE:
                    item = EpisodeItem(name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls)

                case ItemType.PODCAST:
                    item = PodcastItem(name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls)

                case ItemType.PROFILE:
                    item_handle = self._get(
                        ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                        "text", "runs", -1, "text"
                    )
                    item = ProfileItem(name=name, thumbnail_urls=thumbnail_urls, handle=item_handle)

                case ItemType.EP:
                    item = EPItem(name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls)

                case _:
                    return None


        # YouTube Music
        elif ItemStructType.MUSIC_TWO_ROW_ITEM.value in entry_item:
            ds = self._get(entry_item, ItemStructType.MUSIC_TWO_ROW_ITEM.value)
            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnailRenderer", "musicThumbnailRenderer", "thumbnail", "thumbnails")
            )
            name = self._get(ds, "title", "runs", 0, "text")
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
            if item_type is None:
                try:
                    item_type = ItemType(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                            "text", "runs", 0, "text", opt=True
                        )
                    )
                except ValueError:
                    item_type = None

            match item_type:
                case ItemType.ARTIST:
                    subscribers = self._clc_int(self._get(ds, "subtitle", "runs", 0, "text"))
                    item = ArtistItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, subscribers=subscribers
                    )

                case ItemType.ALBUM:
                    release_year = to_int(self._get(ds, "subtitle", "runs", -1, "text", opt=True))
                    item = AlbumItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, release_year=release_year
                    )

                case ItemType.EP:
                    release_year = to_int(self._get(ds, "subtitle", "runs", -1, "text", opt=True))
                    item = EPItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, release_year=release_year
                    )

                case ItemType.YOUTUBE_MUSIC_VIDEO:
                    views = self._clc_int(self._get(ds, "subtitle", "runs", -1, "text"))
                    item = YouTubeMusicVideoItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, views=views
                    )

                case ItemType.YOUTUBE_MUSIC_PLAYLIST:
                    item = YouTubeMusicPlaylistItem(name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls)

                case ItemType.SINGLE:
                    release_year = to_int(self._get(ds, "subtitle", "runs", -1, "text", opt=True))
                    item = SingleItem(
                        name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, release_year=release_year
                    )

                case ItemType.SONG:
                    item = SongItem(name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls)

                case ItemType.EPISODE | ItemType.PODCAST | ItemType.PROFILE:
                    return None

                case _:
                    item = Item(name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls)

        # YouTube Music
        elif ItemStructType.PLAYLIST_PANEL_VIDEO.value in entry_item:
            ds = self._get(entry_item, ItemStructType.PLAYLIST_PANEL_VIDEO.value)
            name = self._get(ds, "title", "runs", -1, "text")
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
            length = self._clc_length(self._get(ds, "lengthText", "runs", -1, "text"))
            thumbnail_urls = self._extract_urls(self._get(ds, "thumbnail", "thumbnails"))
            tmp = self._get(ds, "thumbnail", "thumbnails", -1)
            width = self._get(tmp, "width")
            height = self._get(tmp, "height")
            if width / height == 1:
                item = SongItem(
                    name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, length=length, album_item=None
                )
            else:
                views = self._clc_int(self._get(ds, "longBylineText", "runs", -3, "text", opt=True), opt=True)
                item = YouTubeMusicVideoItem(
                    name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, length=length, views=views
                )

        # YouTube Music
        elif ItemStructType.MUSIC_IMMERSIVE_HEADER.value in entry_item:
            ds = self._get(entry_item, ItemStructType.MUSIC_IMMERSIVE_HEADER.value)
            description = self._extract_description(self._get(ds, "description", "runs", opt=True))
            name = self._get(ds, "title", "runs", 0, "text")
            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails")
            )
            subscribers = self._clc_int(
                self._get(
                    ds, "subscriptionButton", "subscribeButtonRenderer", 
                    "subscriberCountText", "runs", 0, "text"
                )
            )
            item = ArtistItem(
                name=name, subscribers=subscribers, description=description, thumbnail_urls=thumbnail_urls
            )

        # YouTube Music
        elif ItemStructType.MUSIC_DETAIL_HEADER.value in entry_item:
            ds = self._get(entry_item, ItemStructType.MUSIC_DETAIL_HEADER.value)
            try:
                item_type = ItemType(self._get(ds, "subtitle", "runs", 0, "text"))
            except ValueError:
                return None

            name = self._get(ds, "title", "runs", 0, "text")

            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnail", "croppedSquareThumbnailRenderer", "thumbnail", "thumbnails")
            )

            release_year = to_int(self._get(ds, "subtitle", "runs", -1, "text", opt=True))

            if item_type is ItemType.YOUTUBE_MUSIC_PLAYLIST:
                tracks_num = clc_int(self._get(ds, "secondSubtitle", "runs", 2, "text"))
            else:
                tracks_num = clc_int(self._get(ds, "secondSubtitle", "runs", 0, "text"))

            description = self._extract_description(self._get(ds, "description", "runs", opt=True))

            # TODO extract length: X minutes, N hour (?), K seconds (?)

            match item_type:
                case ItemType.ALBUM:
                    item = AlbumItem(
                        name=name, endpoint=None, thumbnail_urls=thumbnail_urls, tracks_num=tracks_num,
                        release_year=release_year, description=description
                    )

                case ItemType.EP:
                    item = EPItem(
                        name=name, endpoint=None, thumbnail_urls=thumbnail_urls, tracks_num=tracks_num, 
                        release_year=release_year, description=description
                    )

                case ItemType.SINGLE:
                    item = SingleItem(
                        name=name, endpoint=None, thumbnail_urls=thumbnail_urls, tracks_num=tracks_num, 
                        release_year=release_year, description=description
                    )

                case ItemType.YOUTUBE_MUSIC_PLAYLIST:
                    views = self._clc_int(self._get(ds, "secondSubtitle", "runs", 0, "text"))
                    item = YouTubeMusicPlaylistItem(
                        name=name, endpoint=None, thumbnail_urls=thumbnail_urls, tracks_num=tracks_num,
                        release_year=release_year, description=description, views=views
                    )

                case _:
                    return None

        # YouTube Music
        elif ItemStructType.MUSIC_VISUAL_HEADER.value in entry_item:
            ds = self._get(entry_item, ItemStructType.MUSIC_VISUAL_HEADER.value)
            name = self._get(ds, "title", "runs", -1, "text")
            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails")
            )
            item = Item(name=name, thumbnail_urls=thumbnail_urls)

        # YouTube Music
        elif ItemStructType.MUSIC_MULTI_ROW_LIST_ITEM.value in entry_item:
            ds = self._get(entry_item)
            name = self._get(ds, "title", "runs", 0, "text")
            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails")
            )
            endpoint = self._extract_endpoint(self._get(ds, "title", "runs", 0, "navigationEndpoint"))
            item = Item(name=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint)

        # YouTube (custom)
        elif ItemStructType.NEXT_PRIMARY_VIDEO.value in entry_item:
            ds = self._get(entry_item, ItemStructType.NEXT_PRIMARY_VIDEO.value)
            video_data = self._get(ds, ItemType.YOUTUBE_VIDEO.value)
            item_name = self._get(video_data, "title", "runs", 0, "text")
            item_views = self._clc_views(
                self._get(
                    video_data, "viewCount", "videoViewCountRenderer", "viewCount", "simpleText"
                )
            )

            item_endpoint = WatchEndpoint(
                video_id=self._get(
                    video_data, "videoActions", "menuRenderer", "topLevelButtons", 0, 
                    "segmentedLikeDislikeButtonViewModel", "likeButtonViewModel", "likeButtonViewModel",
                    "toggleButtonViewModel", "toggleButtonViewModel", "defaultButtonViewModel", 
                    "buttonViewModel", "onTap", "serialCommand", "commands", 1, "innertubeCommand",
                    "modalEndpoint", "modal", "modalWithTitleAndButtonRenderer", "button",
                    "buttonRenderer", "navigationEndpoint", "signInEndpoint", "nextEndpoint",
                    "likeEndpoint", "target", "videoId"
                )
            )

            item_description = self._extract_description(
                self._get(ds, ItemType.CHANNEL.value, "attributedDescription")
            )

            channel_data = self._get(ds, ItemType.CHANNEL.value, "owner", "videoOwnerRenderer")
            channel_thumbnail_urls = self._extract_urls(self._get(channel_data, "thumbnail", "thumbnails"))
            channel_name = self._get(channel_data, "title", "runs", 0, "text")
            channel_endpoint = self._extract_endpoint(self._get(channel_data, "navigationEndpoint"))
            channel_subscribers = self._clc_int(self._get(channel_data, "subscriberCountText", "simpleText"))
            channel_item = ChannelItem(
                name=channel_name, thumbnail_urls=channel_thumbnail_urls,
                endpoint=channel_endpoint, subscribers=channel_subscribers
            )

            item = YouTubeVideoItem(
                name=item_name, views=item_views, endpoint=item_endpoint, 
                channel_item=channel_item, description=item_description
            )

        elif ItemStructType.CHANNEL_VIDEO_PLAYER.value in entry_item:
            ds = self._get(entry_item, ItemStructType.CHANNEL_VIDEO_PLAYER.value)
            name = self._get(ds, "title", "runs", 0, "text")
            description = self._extract_description(self._get(ds, "description", "runs"))
            views = self._clc_views(self._get(ds, "viewCountText", "simpleText"))
            endpoint = self._extract_endpoint(self._get(ds, "title", "runs", 0, "navigationEndpoint"))
            item = YouTubeVideoItem(name=name, endpoint=endpoint, description=description, views=views)

        # YouTube
        elif (
            ItemStructType.CHANNEL.value in entry_item
            or ItemStructType.VIDEO.value in entry_item
            or ItemStructType.PLAYLIST_VIDEO.value in entry_item
            or ItemStructType.PLAYLIST.value in entry_item
            or ItemStructType.RADIO.value in entry_item
            or ItemStructType.COMPACT_VIDEO.value in entry_item
            or ItemStructType.COMPACT_RADIO.value in entry_item
            or ItemStructType.COMPACT_PLAYLIST.value in entry_item
            or ItemStructType.GRID_VIDEO.value in entry_item
            or ItemStructType.GRID_CHANNEL.value in entry_item
            or ItemStructType.GRID_PLAYLIST.value in entry_item
        ):
            ds = self._get(entry_item, list(entry_item.keys())[0])
            name = self._get(ds, "title", "simpleText", opt=True)
            if name is None:
                name = self._get(ds, "title", "runs", 0, "text")
            thumbnail_urls = self._extract_urls(self._get(ds, "thumbnail", "thumbnails", opt=True))
            if thumbnail_urls is None:
                thumbnail_urls = self._extract_urls(self._get(ds, "thumbnails", 0, "thumbnails"))
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))

            if (
                ItemStructType.PLAYLIST_VIDEO.value in entry_item
                or ItemStructType.COMPACT_PLAYLIST.value in entry_item
                or ItemStructType.COMPACT_VIDEO.value in entry_item
                or ItemStructType.GRID_VIDEO.value in entry_item
                or ItemStructType.VIDEO.value in entry_item
            ):
                views = self._clc_views(self._get(ds, "viewCountText", "simpleText", opt=True))
                if views is None:
                    views = self._clc_int(self._get(ds, "videoInfo", "runs", 0, "text", opt=True))

                length = self._clc_length(self._get(ds, "lengthText", "simpleText", opt=True))
                if length is None:
                    length = self._clc_length(
                        self._get(
                            ds, "thumbnailOverlays", 0, "thumbnailOverlayTimeStatusRenderer",
                            "text", "simpleText", opt=True
                        )
                    )

                description = self._extract_description(
                    self._get(ds, "detailedMetadataSnippets", 0, "snippetText", "runs", opt=True)
                )
                published_time = self._get(ds, "publishedTimeText", "simpleText", opt=True)
                if published_time is None:
                    published_time = self._get(ds, "videoInfo", "runs", -1, "text", opt=True)

                channel_data = self._get(ds, "shortBylineText", "runs", 0, opt=True)
                if channel_data is None:
                    channel_data = self._get(ds, "longBylineText", "runs", 0, opt=True)

                if channel_data is not None:
                    channel_name = self._get(channel_data, "text")
                    channel_endpoint = self._extract_endpoint(self._get(channel_data, "navigationEndpoint"))
                    channel_thumbnail_urls = self._extract_urls(
                        self._get(
                            ds, "channelThumbnailSupportedRenderers", "channelThumbnailWithLinkRenderer",
                            "thumbnail", "thumbnails", opt=True
                        )
                    )
                    channel_item = ChannelItem(
                        name=channel_name, endpoint=channel_endpoint, thumbnail_urls=channel_thumbnail_urls
                    )
                else:
                    channel_item = None

                item = YouTubeVideoItem(
                    name=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint, views=views, length=length, 
                    channel_item=channel_item, description=description, published_time=published_time
                )

            elif (
                ItemStructType.CHANNEL.value in entry_item 
                or ItemStructType.GRID_CHANNEL.value in entry_item
            ):
                subscribers = self._clc_int(
                    self._get(ds, "subscriberCountText", "simpleText", opt=True), opt=True
                )
                videos_num = self._clc_int(self._get(ds, "videoCountText", "runs", 0, "text", opt=True))
            
                item = ChannelItem(
                    name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, subscribers=subscribers, 
                    videos_num=videos_num 
                )

            elif ItemStructType.GRID_PLAYLIST.value in entry_item:
                videos_num = self._clc_int(self._get(ds, "videoCountText", "runs", 0, "text"))

                channel_data = self._get(ds, "shortBylineText", "runs", 0, opt=True)
                channel_name = self._get(channel_data, "text")
                channel_endpoint = self._extract_endpoint(self._get(channel_data, "navigationEndpoint"))
                channel_item = ChannelItem(name=channel_name, endpoint=channel_endpoint)

                item = YouTubePlaylistItem(
                    name=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, channel_item=channel_item, 
                    videos_num=videos_num
                )

            elif ItemStructType.COMPACT_RADIO.value in entry_item:
                item = RadioItem(name=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint)

            elif ItemStructType.PLAYLIST.value in entry_item:
                video_items = self._extract_child_videos(self._get(ds, "videos"))
                videos_num = self._get(ds, "videoCount")

                channel_data = self._get(ds, "shortBylineText", "runs", 0, opt=True)
                channel_name = self._get(channel_data, "text")
                channel_endpoint = self._extract_endpoint(self._get(channel_data, "navigationEndpoint"))
                channel_item = ChannelItem(name=channel_name, endpoint=channel_endpoint)

                item = YouTubePlaylistItem(
                    name=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint, video_items=video_items,
                    channel_item=channel_item, videos_num=videos_num
                )

            else:  # ItemStructType.RADIO
                video_items = self._extract_child_videos(self._get(ds, "videos"))
                item = RadioItem(
                    name=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint, video_items=video_items
                )

        elif ItemStructType.REEL_ITEM.value in entry_item:
            ds = self._get(entry_item, ItemStructType.REEL_ITEM.value)
            name = self._get(ds, "headline", "simpleText")
            thumbnail_urls = self._extract_urls(self._get(ds, "thumbnail", "thumbnails"))
            endpoint = WatchEndpoint(video_id=self._get(ds, "videoId"))
            item = YouTubeVideoItem(name=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint)

        elif ItemStructType.WATCH_CARD_COMPACT_VIDEO.value in entry_item:
            ds = self._get(entry_item, ItemStructType.WATCH_CARD_COMPACT_VIDEO.value)
            name = self._get(ds, "title", "simpleText")
            length = self._clc_length(self._get(ds, "lengthText", "simpleText"))
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
            views = self._clc_int(self._get(ds, "subtitle", "simpleText"))
            tmp = self._get(ds, "subtitle", "simpleText").split(TextDivisorType.BULLET_POINT.value)
            published_time = tmp[1] if len(tmp) > 1 else None
            channel_data = self._get(ds, "byline", "runs", 0)
            channel_name = self._get(channel_data, "text")
            channel_endpoint = self._extract_endpoint(self._get(channel_data, "navigationEndpoint"))
            channel_item = ChannelItem(name=channel_name, endpoint=channel_endpoint)
            item = YouTubeVideoItem(
                name=name, endpoint=endpoint, length=length, views=views, 
                channel_item=channel_item, published_time=published_time
            )

        elif ItemStructType.SEARCH_REFINEMENT_CARD.value in entry_item:
            ds = self._get(entry_item, ItemStructType.SEARCH_REFINEMENT_CARD.value)
            name = self._get(ds, "query", "runs", 0, "text")
            thumbnail_urls = self._extract_urls(self._get(ds, "thumbnail", "thumbnails"))
            endpoint = WatchEndpoint(
                playlist_id=self._get(ds, "searchEndpoint", "watchPlaylistEndpoint", "playlistId")
            )
            item = AlbumItem(name=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint)

        # Item structures ignored
        elif (
            ItemStructType.AUTOMIX_PREVIEW_VIDEO.value in entry_item
            or ItemStructType.RELATED_CHIP_CLOUD.value in entry_item
            or ItemStructType.AD_SLOT.value in entry_item
            or ItemStructType.CONTINUATION_ITEM.value in entry_item
            or ItemStructType.MESSAGE.value in entry_item
        ):
            return None

        else:
            raise AccessError(data=entry_item)

        return item

    @return_on_input_none
    @_handle_exception
    def _extract_endpoint(self, data: Dict) -> Optional[Endpoint]:
        """
        Method for extracting an endpoint from the specified dictionary.
        @param data: A portion of the data provided by InnerTube containing
        the details of an endpoint object.
        @return: An Endpoint object otherwise None if no registered endpoint
        structure was detected in the specified dictionary.
        """
        if EndpointType.BROWSE.value in data:
            browse_endpoint_data = self._get(data, "browseEndpoint")
            browse_id = self._get(browse_endpoint_data, "browseId")
            params = self._get(browse_endpoint_data, "params", opt=True)

            canonical_base_url = self._get(browse_endpoint_data, "canonicalBaseUrl", opt=True)
            if canonical_base_url is None:
                endpoint = BrowseEndpoint(browse_id=browse_id, params=params)
            else:
                endpoint = YouTubeBrowseEndpoint(
                    browse_id=browse_id, params=params, canonical_base_url=canonical_base_url
                )

        elif EndpointType.WATCH.value in data:
            video_id = self._get(data, EndpointType.WATCH.value, "videoId")
            playlist_id = self._get(data, EndpointType.WATCH.value, "playlistId", opt=True)
            params = self._get(data, EndpointType.WATCH.value, "params", opt=True)
            endpoint = WatchEndpoint(video_id=video_id, playlist_id=playlist_id, params=params)

        elif EndpointType.REEL_WATCH.value in data:
            video_id = self._get(data, EndpointType.REEL_WATCH.value, "videoId")
            playlist_id = self._get(data, EndpointType.REEL_WATCH.value, "playlistId", opt=True)
            params = self._get(data, EndpointType.REEL_WATCH.value, "params", opt=True)
            endpoint = WatchEndpoint(video_id=video_id, playlist_id=playlist_id, params=params)

        elif EndpointType.SEARCH.value in data:
            query = self._get(data, EndpointType.SEARCH.value, "query")
            params = self._get(data, EndpointType.SEARCH.value, "params", opt=True)
            endpoint = SearchEndpoint(query=query, params=params)

        elif EndpointType.URL.value in data:
            url = self._get(data, EndpointType.URL.value, "url")
            params = self._get(data, EndpointType.URL.value, "params", opt=True)
            endpoint = UrlEndpoint(url=url, params=params)

        elif EndpointType.CONTINUATION.value in data:
            continuation = self._get(data, EndpointType.CONTINUATION.value, "continuationCommand", "token")
            endpoint = ContinuationEndpoint(continuation=continuation)

        else:
            raise AccessError(data=data)

        return endpoint

    @return_on_input_none
    @_handle_exception
    def _clc_length(self, string: str) -> Optional[time]:
        """
        Wrapper to the innertube_de.utils.clc_length function that allows
        its decoration without modifying the original code.
        @param string: The string to pass to the innertube_de.utils.clc_length function
        @return: The result of the innertube_de.utils.clc_length function
        """
        return clc_length(string)

    @return_on_input_none
    @_handle_exception
    def _clc_publication_date(self, string: str) -> Optional[date]:
        """
        Wrapper to the innertube_de.utils.clc_publication_date function
        that allows its decoration without modifying the original code
        @param string: The string to pass to the innertube_de.utils.clc_publication_date function
        @return: The result of the innertube_de.utils.clc_publication_date function
        """
        return clc_publication_date(string)

    @return_on_input_none
    @_handle_exception
    def _clc_int(self, string: str) -> Optional[int]:
        """
        Wrapper to the innertube_de.utils.clc_int function that allows
        its decoration without modifying the original code
        @param string: The string to pass to the innertube_de.utils.clc_int method
        @return: The result of the innertube.utils.clc_int function
        """
        return clc_int(string)

    @return_on_input_none
    @_handle_exception
    def _clc_views(self, string: str) -> Optional[int]:
        return clc_views(string)

    @_handle_exception
    def _get(self, ds: Union[List, Dict], *keys) -> Optional[Any]:
        """
        Wrapper to the innertube_de.utils.get function that allows
        its decoration without modifying the original code.
        In this case, since the innertube_de.utils.get function is recursive,
        it avoids invoking the code contained in the decorators at each
        recursive call and therefore, in the case of the _handle_exception decorator,
        to set the opt field to the default value for each recursive call.
        @param ds: The dictionary to pass to the innertube.utils.get function
        @param keys: All remaining parameters used to access the specified dictionary
        by the innertube_de.utils.get function.
        @return: The result of the innertube_de.utils.get function
        """
        return get(ds, *keys)

    @return_on_input_none
    @_handle_exception
    def _extract_description(self, ds: Union[List[Dict], Dict]) -> List[Tuple[str, Optional[Endpoint]]]:
        if isinstance(ds, List):
            return [
                (self._get(e, "text"), self._extract_endpoint(self._get(e, "navigationEndpoint", opt=True))) 
                for e in ds
            ]
        else:
            content = self._get(ds, "content")
            cmds = self._get(ds, "commandRuns", opt=True)
            if cmds is None:
                return [(content, None)]
            description: List[Tuple[str, Optional[Endpoint]]] = []
            index = 0
            for entry in cmds:
                start = self._get(entry, "startIndex")
                end = start + int(self._get(entry, "length"))
                endpoint = self._extract_endpoint(self._get(entry, "onTap", "innertubeCommand"))
                if len(content[index:start]) > 0:
                    description.append((content[index: start], None))
                description.append((content[start: end], endpoint))
                index = end
            if index < len(content):
                description.append((content[index:], None))
            return description

    @return_on_input_none
    def _extract_urls(self, urls_data: List[Dict]) -> List[Dict]:
        urls = urls_data if self.include_all_urls is True else [self._get(urls_data, -1)]
        for entry in urls:
            if not entry["url"].startswith("https:"):
                entry["url"] = f"https:{entry['url']}"
        return urls

    def _extract_child_videos(self, videos_data: List[Dict]) -> List[YouTubeVideoItem]:
        videos: List[YouTubeVideoItem] = []
        for video_data in videos_data:
            video_data = self._get(video_data, "childVideoRenderer")
            name = self._get(video_data, "title", "simpleText")
            endpoint = self._extract_endpoint(self._get(video_data, "navigationEndpoint"))
            length = self._clc_length(self._get(video_data, "lengthText", "simpleText"))
            videos.append(YouTubeVideoItem(name=name, endpoint=endpoint, length=length))
        return videos
