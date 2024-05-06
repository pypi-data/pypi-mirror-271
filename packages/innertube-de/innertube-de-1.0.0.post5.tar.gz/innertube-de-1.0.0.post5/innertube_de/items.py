from dataclasses import dataclass
from abc import ABC
from datetime import date, time
from typing import List, Optional, Dict, Tuple
from innertube_de.types import ItemType
from innertube_de.endpoints import Endpoint
from innertube_de import utils


@dataclass(kw_only=True)
class Item:
    name: Optional[str] = None
    thumbnail_urls: Optional[List[Dict]] = None
    endpoint: Optional[Endpoint] = None
    description: Optional[List[Tuple[str, Optional[Endpoint]]]] = None

    def dump(self) -> Dict:
        return dict(
            type=None,
            name=self.name,
            endpoint=None if self.endpoint is None else self.endpoint.dump(),
            thumbnail_urls=self.thumbnail_urls,
            description=[
                (text, None if endpoint is None else endpoint.dump()) for text, endpoint in self.description
            ] if self.description is not None else None
        )

    def load(self, data: Dict) -> None:
        self.name = data["name"]
        self.thumbnail_urls = data["thumbnail_urls"]
        self.description = [
            (text, utils.get_endpoint(endpoint_data)) 
            for text, endpoint_data in data["description"]
        ] if data["description"] is not None else None
        self.endpoint = utils.get_endpoint(data["endpoint"])


@dataclass(kw_only=True)
class ArtistItem(Item):
    subscribers: Optional[int] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(type=ItemType.ARTIST.value, subscribers=self.subscribers))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.subscribers = data["subscribers"]


@dataclass(kw_only=True)
class ChannelItem(ArtistItem):
    videos_num: Optional[int] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            type=ItemType.CHANNEL.value,
            videos_num=self.videos_num,
            subscribers=self.subscribers
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.videos_num = data["videos_num"]


@dataclass(kw_only=True)
class VideoItem(Item, ABC):
    length: Optional[time] = None 
    views: Optional[int] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            views=self.views,
            length=None if self.length is None else dict(
                hour=self.length.hour,
                minute=self.length.minute,
                second=self.length.second
            )
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.views = data["views"]
        self.length = utils.get_length(data["length"])


@dataclass(kw_only=True)
class YouTubeVideoItem(VideoItem):
    channel_item: Optional[ChannelItem] = None
    published_time: Optional[str] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            type=ItemType.YOUTUBE_VIDEO.value,
            channel_item=None if self.channel_item is None else self.channel_item.dump(),
            published_time=self.published_time
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.channel_item = utils.get_item(data["channel_item"])
        self.published_time = data["published_time"]


@dataclass(kw_only=True)
class YouTubeMusicVideoItem(VideoItem):
    artist_items: Optional[List[ArtistItem]] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            type=ItemType.YOUTUBE_MUSIC_VIDEO.value,
            artist_items=[a.dump() for a in self.artist_items] if self.artist_items is not None else None
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.artist_items = utils.get_items(data["artist_items"])  # type: ignore


@dataclass(kw_only=True)
class AlbumItem(Item):
    release_year: Optional[int] = None
    length: Optional[time] = None
    tracks_num: Optional[int] = None
    artist_items: Optional[List[ArtistItem]] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            type=ItemType.ALBUM.value,
            tracks_num=self.tracks_num,
            release_year=self.release_year,
            artist_items=[a.dump() for a in self.artist_items] if self.artist_items is not None else None,
            length=None if self.length is None else dict(
                hour=self.length.hour,
                minute=self.length.minute,
                second=self.length.second
            )
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.tracks_num = data["tracks_num"]
        self.release_year = data["release_year"]
        self.artist_items = utils.get_items(data["artist_items"])  # type: ignore
        self.length = utils.get_length(data["length"])


@dataclass(kw_only=True)
class EPItem(AlbumItem):
    """ """

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(type=ItemType.EP.value))
        return d


@dataclass(kw_only=True)
class RadioItem(Item):
    video_items: Optional[List[YouTubeVideoItem]] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            type=ItemType.RADIO.value,
            video_items=[
                video.dump() for video in self.video_items
            ] if self.video_items is not None else None
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.video_items = utils.get_items(data["video_items"])  # type: ignore


@dataclass(kw_only=True)
class YouTubePlaylistItem(Item):
    channel_item: Optional[ChannelItem] = None
    videos_num: Optional[int] = None 
    video_items: Optional[List[YouTubeVideoItem]] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            type=ItemType.YOUTUBE_PLAYLIST.value,
            videos_num=self.videos_num,
            video_items=[
                video.dump() for video in self.video_items
            ] if self.video_items is not None else None,
            channel_item=None if self.channel_item is None else self.channel_item.dump()
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.videos_num = data["videos_num"]
        self.channel_item = utils.get_item(data["channel_item"])  # type: ignore
        self.video_items = utils.get_items(data["video_items"])   # type: ignore


@dataclass(kw_only=True)
class YouTubeMusicPlaylistItem(AlbumItem):
    views: Optional[int] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            type=ItemType.YOUTUBE_MUSIC_PLAYLIST.value,
            views=self.views
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.views = data["views"]


@dataclass(kw_only=True)
class SingleItem(AlbumItem):
    """ """

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(type=ItemType.SINGLE.value))
        return d


@dataclass(kw_only=True)
class SongItem(Item):
    length: Optional[time] = None
    reproductions: Optional[int] = None
    album_item: Optional[AlbumItem] = None
    artist_items: Optional[List[ArtistItem]] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            type=ItemType.SONG.value,
            reproductions=self.reproductions,
            album_item=None if self.album_item is None else self.album_item.dump(),
            artist_items=[a.dump() for a in self.artist_items] if self.artist_items is not None else None,
            length=None if self.length is None else dict(
                hour=self.length.hour,
                minute=self.length.minute,
                second=self.length.second
            )
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.reproductions = data["reproductions"]
        self.artist_items = utils.get_items(data["artist_items"])  # type: ignore
        self.album_item = utils.get_item(data["album_item"])
        self.length = utils.get_length(data["length"])


@dataclass(kw_only=True)
class ProfileItem(Item):
    handle: Optional[str] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            type=ItemType.PROFILE.value,
            handle=self.handle
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.handle = data["handle"]


@dataclass(kw_only=True)
class PodcastItem(Item):
    length: Optional[time] = None
    artist_items: Optional[List[ArtistItem]] = None


    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            type=ItemType.PODCAST.value,
            artist_items=[a.dump for a in self.artist_items] if self.artist_items is not None else None,
            length=None if self.length is None else dict(
                hour=self.length.hour,
                minute=self.length.minute,
                second=self.length.second
            )
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.artist_items = utils.get_items(data["artist_items"])  # type: ignore
        self.length = utils.get_length(data["length"])


@dataclass(kw_only=True)
class EpisodeItem(Item):
    publication_date: Optional[date] = None
    length: Optional[time] = None
    artist_items: Optional[List[ArtistItem]] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            type=ItemType.EPISODE.value,
            artist_items=[a.dump() for a in self.artist_items] if self.artist_items is not None else None,
            publication_date=None if self.publication_date is None else dict(
                month=self.publication_date.month,
                day=self.publication_date.day,
                year=self.publication_date.year
            ),
            length=None if self.length is None else dict(
                hour=self.length.hour,
                minute=self.length.minute,
                second=self.length.second
            )
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.artist_items = utils.get_items(data["artist_items"])  # type: ignore
        self.publication_date = utils.get_publication_date(data["publication_date"])
        self.length = utils.get_length(data["length"])
