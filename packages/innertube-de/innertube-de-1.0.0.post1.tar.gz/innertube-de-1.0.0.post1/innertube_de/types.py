from enum import Enum


class _Enum(Enum):
    @classmethod
    def has_value(cls, value):
        return any(member.value == value for member in cls)


class _StrEnum(str, _Enum):
    """ """


class ResultStructType(_StrEnum):
    # YouTube Music
    TABBED_SEARCH_RESULTS = "tabbedSearchResultsRenderer"
    SINGLE_COLUMN_BROWSE_RESULTS = "singleColumnBrowseResultsRenderer"
    SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT = "singleColumnMusicWatchNextResultsRenderer"
    TWO_COLUMN_BROWSE_RESULT = "twoColumnBrowseResultsRenderer"

    # YouTube
    TWO_COLUMN_SEARCH_RESULTS = "twoColumnSearchResultsRenderer"
    TWO_COLUMN_WATCH_NEXT_RESULTS = "twoColumnWatchNextResults"
    ON_RESPONSE_RECEIVED_ENDPOINTS = "onResponseReceivedEndpoints"


class ContinuationStrucType(_StrEnum):
    # YouTube Music
    MUSIC_SHELF = "musicShelfContinuation"
    MUSIC_PLAYLIST_SHELF = "musicPlaylistShelfContinuation"
    SECTION_LIST = "sectionListContinuation"

    # YouTube Music / YouTube
    CONTINUATION = "continuationContents"


class ShelfStructType(_StrEnum):
    # YouTube Music
    GRID = "gridRenderer"
    MUSIC_SHELF = "musicShelfRenderer"
    MUSIC_CARD_SHELF = "musicCardShelfRenderer"
    MUSIC_CAROUSEL_SHELF = "musicCarouselShelfRenderer"
    MUSIC_DESCRIPTION_SHELF = "musicDescriptionShelfRenderer"
    MUSIC_PLAYLIST_SHELF = "musicPlaylistShelfRenderer"
    ITEM_SECTION = "itemSectionRenderer"
    PLAYLIST_PANEL = "playlistPanelRenderer"
    SHOWING_RESULTS_FOR = "showingResultsForRenderer"

    # YouTube
    SHELF = "shelfRenderer"
    SECONDARY_RESULTS = "secondaryResults"
    PLAYLIST_VIDEO_LIST_CONTINUATION = "playlistVideoListContinuation"
    REEL_SHELF = "reelShelfRenderer"
    VERTICAL_WATCH_CARD_LIST = "verticalWatchCardListRenderer"
    HORIZONTAL_CARD_LIST_RENDERER = "horizontalCardListRenderer"

    # YouTube - custom
    NEXT_PRIMARY_SHELF = "nextPrimaryShelf"
    CHANNEL_SHELF = "channelShelf"


class ItemStructType(_StrEnum):
    # YouTube Music
    MUSIC_TWO_ROW_ITEM = "musicTwoRowItemRenderer"
    MUSIC_VISUAL_HEADER = "musicVisualHeaderRenderer"
    MUSIC_RESPONSIVE_LIST_ITEM = "musicResponsiveListItemRenderer"
    MUSIC_DETAIL_HEADER = "musicDetailHeaderRenderer"
    MUSIC_IMMERSIVE_HEADER = "musicImmersiveHeaderRenderer"
    MUSIC_MULTI_ROW_LIST_ITEM = "musicMultiRowListItemRenderer"
    PLAYLIST_PANEL_VIDEO = "playlistPanelVideoRenderer"
    PLAYLIST_EXPANDABLE_MESSAGE = "playlistExpandableMessageRenderer"

    # YouTube Music - ignored
    AUTOMIX_PREVIEW_VIDEO = "automixPreviewVideoRenderer"
    MESSAGE = "messageRenderer"

    # YouTube
    CONTINUATION_ITEM = "continuationItemRenderer"
    WATCH_CARD_COMPACT_VIDEO = "watchCardCompactVideoRenderer"
    SEARCH_REFINEMENT_CARD = "searchRefinementCardRenderer"
    VIDEO = "videoRenderer"
    CHANNEL = "channelRenderer"
    RADIO = "radioRenderer"
    PLAYLIST = "playlistRenderer"
    PLAYLIST_VIDEO = "playlistVideoRenderer"
    CHANNEL_VIDEO_PLAYER = "channelVideoPlayerRenderer"
    COMPACT_VIDEO = "compactVideoRenderer"
    COMPACT_RADIO = "compactRadioRenderer"
    COMPACT_PLAYLIST = "compactPlaylistRenderer"
    GRID_PLAYLIST = "gridPlaylistRenderer"
    GRID_VIDEO = "gridVideoRenderer"
    GRID_CHANNEL = "gridChannelRenderer"
    REEL_ITEM = "reelItemRenderer"

    # YouTube - custom
    NEXT_PRIMARY_VIDEO = "nextPrimaryVideo"

    # YouTube - ignored
    RELATED_CHIP_CLOUD = "relatedChipCloudRenderer"
    AD_SLOT = "adSlotRenderer"


class ItemType(_StrEnum):
    # YouTube Music
    SONG = "Song"       
    SINGLE = "Single"
    YOUTUBE_MUSIC_PLAYLIST = "YouTubeMusicPlaylist"
    YOUTUBE_MUSIC_VIDEO = "YouTubeMusicVideo"
    ALBUM = "Album"
    EP = "EP"
    ARTIST = "Artist"
    EPISODE = "Episode"
    PROFILE = "Profile"
    PODCAST = "Podcast"

    # YouTube
    CHANNEL = "Channel"
    RADIO = "Radio"
    YOUTUBE_VIDEO = "YouTubeVideo"
    YOUTUBE_PLAYLIST = "YouTubePlaylist"

    def __repr__(self) -> str:
        return f"ItemType.{str(self)}"

    def __str__(self) -> str:
        return self.value


class ShelfType(_StrEnum):
    SHELF = "Shelf"
    CARD_SHELF = "CardShelf"

    def __repr__(self) -> str:
        return f"ShelfType.{str(self)}"

    def __str__(self) -> str:
        return self.value


class EndpointType(_StrEnum):
    WATCH = "watchEndpoint"
    BROWSE = "browseEndpoint"
    SEARCH = "searchEndpoint"
    CONTINUATION = "continuationEndpoint"
    URL = "urlEndpoint"
    REEL_WATCH = "reelWatchEndpoint"

    # Custom endpoint type
    YOUTUBE_BROWSE = "youTubeBrowseEndpoint"

    def __repr__(self) -> str:
        return f"EndpointType.{str(self)}"

    def __str__(self) -> str:
        return self.value


class TextDivisorType(_StrEnum):
    BULLET_POINT = "\u2022"
