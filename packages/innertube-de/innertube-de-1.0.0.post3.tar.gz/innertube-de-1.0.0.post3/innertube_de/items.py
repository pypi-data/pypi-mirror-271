from abc import ABC
from datetime import date, time
from typing import List, Optional, Dict, Tuple
from innertube_de.types import ItemType
from innertube_de.endpoints import Endpoint
from innertube_de import utils


class Item:
    """
    Base class of items. Contains data common to all other defined Item types.
    """
    def __init__(
            self,
            name: Optional[str] = None,
            thumbnail_url: Optional[List[Dict]] = None,
            endpoint: Optional[Endpoint] = None,
            description: Optional[List[Tuple[str, Optional[Endpoint]]]] = None,
    ) -> None:
        """
        Initialize this object with the specified parameters.
        @param name: The name of the item.
        @param thumbnail_url: The URL of the cover of this item.
        @param endpoint: The associated Endpoint object.
        @param description: A description of this item.
        """
        self.name = name
        self.thumbnail_url = thumbnail_url
        self.endpoint = endpoint
        self.description = description

    def __repr__(self) -> str:
        return (
            "Item{"
            f"name={self.name}, "
            f"endpoint={self.endpoint}, "
            f"thumbnail_url={self.thumbnail_url}, "
            f"description={self.description}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.name, self.thumbnail_url, self.endpoint, self.description, type(self)))

    def dump(self) -> Dict:
        """
        Serialize this object.
        @return: A dictionary that describes the state of this object.
        """
        return {
            "type": None,
            "name": self.name,
            "endpoint": None if self.endpoint is None else self.endpoint.dump(),
            "thumbnail_url": self.thumbnail_url,
            "description": [
                (text, None if endpoint is None else endpoint.dump()) for text, endpoint in self.description
            ] if self.description is not None else None
        }

    def load(self, data: Dict) -> None:
        """
        Deserialize this object with the specified dictionary.
        @param data: The dictionary containing the data.
        @return: None
        """
        self.name = data["name"]
        self.thumbnail_url = data["thumbnail_url"]
        self.description = [
            (text, utils.get_endpoint(endpoint_data)) 
            for text, endpoint_data in data["description"]
        ] if data["description"] is not None else None
        self.endpoint = utils.get_endpoint(data["endpoint"])


class ItemWithSubscribers(Item, ABC):
    def __init__(self, subscribers: Optional[int] = None, *args, **kwargs) -> None:
        """
        Initialize this object with the specified parameters.
        @param subscribers: The number of subscribers of this ArtistItem object.
        @param args: The positional arguments to pass to the constructor of the Item class.
        @param kwargs: The key arguments to pass to the constructor of the Item class.
        """
        super().__init__(*args, **kwargs)
        self.subscribers = subscribers

    def __repr__(self) -> str:
        return f"{super().__repr__()[:-1]}, subscribers={self.subscribers}" "}"

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) and self.subscribers == __value.subscribers

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.subscribers)

    def dump(self) -> Dict:
        d = super().dump()
        d.update({"subscribers": self.subscribers})
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.subscribers = data["subscribers"]


class ChannelItem(ItemWithSubscribers):
    def __init__(self, videos_num: Optional[int] = None, *args, **kwargs) -> None:
        """
        Initialize this object with the specified parameters.
        @param videos_num: 
        @param args: The positional arguments to pass to the constructor of the Item class.
        @param kwargs: The key arguments to pass to the constructor of the Item class.
        """
        super().__init__(*args, **kwargs)
        self.videos_num = videos_num

    def __repr__(self) -> str:
        return f"Channel{super().__repr__()[:-1]}, videos_num={self.videos_num}" "}"

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) and self.videos_num == __value.videos_num

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.videos_num)

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.CHANNEL.value,
            "videos_num": self.videos_num
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.videos_num = data["videos_num"]


class ArtistItem(ItemWithSubscribers):
    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize this object with the specified parameters.
        @param args: The positional arguments to pass to the constructor of the Item class.
        @param kwargs: The key arguments to pass to the constructor of the Item class.
        """
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"Artist{super().__repr__()}"

    def dump(self) -> Dict:
        d = super().dump()
        d.update({"type": ItemType.ARTIST.value})
        return d


class VideoItem(Item, ABC):
    def __init__(self, length: Optional[time] = None, views: Optional[int] = None, *args, **kwargs) -> None:
        """
        Initialize this object with the specified parameters.
        @param length: An object of the time class that describes the duration of the video.
        @param views: An integer that describes the number of views of the video.
        @param args: The positional arguments to pass to the constructor of the Item class.
        @param kwargs: The key arguments to pass to the constructor of the Item class.
        """
        super().__init__(*args, **kwargs)
        self.length = length
        self.views = views

    def __repr__(self) -> str:
        return f"Video{super().__repr__()[:-1]}, length={self.length}, views={self.views}" "}"

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) and self.length == __value.length and self.views == __value.views

    def __hash__(self) -> int:
        return super().__hash__() ^ hash((self.length, self.views))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "views": self.views,
            "length": None if self.length is None else {
                "hour": self.length.hour,
                "minute": self.length.minute,
                "second": self.length.second
            }
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.views = data["views"]
        self.length = utils.get_length(data["length"])


class YouTubeVideoItem(VideoItem):
    def __init__(
                self, 
                channel_item: Optional[ChannelItem] = None,
                published_time: Optional[str] = None,
                *args, 
                **kwargs
        ) -> None:
        super().__init__(*args, **kwargs)
        self.channel_item = channel_item
        self.published_time = published_time

    def __repr__(self) -> str:
        return (
            f"YouTube{super().__repr__()[:-1]}, "
            f"channel_item={self.channel_item}, "
            f"published_time={self.published_time}" 
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        return (
            super().__eq__(__value) 
            and self.channel_item == __value.channel_item
            and self.published_time == __value.published_time
        )

    def __hash__(self) -> int:
        return super().__hash__() ^ hash((self.channel_item, self.published_time))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.YOUTUBE_VIDEO.value,
            "channel_item": None if self.channel_item is None else self.channel_item.dump(),
            "published_time": self.published_time
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.channel_item = utils.get_item(data["channel_item"])
        self.published_time = data["published_time"]


class YouTubeMusicVideoItem(VideoItem):
    def __init__(self, artist_items: Optional[List[ArtistItem]] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.artist_items = artist_items

    def __repr__(self) -> str:
        return f"YouTubeMusic{super().__repr__()[:-1]}, artist_items={self.artist_items}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.artist_items == __value.artist_items
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.name, self.thumbnail_url, self.endpoint, self.description, self.artist_items))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.YOUTUBE_MUSIC_VIDEO.value,
            "artist_items": [a.dump() for a in self.artist_items]
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.artist_items = utils.get_items(data["artist_items"])


class AlbumItem(Item):
    def __init__(
            self,
            release_year: Optional[int] = None,
            length: Optional[time] = None,
            tracks_num: Optional[int] = None,
            artist_items: Optional[List[ArtistItem]] = None,
            *args,
            **kwargs,
    ) -> None:
        """
        Initialize this object with the specified parameters.
        @param release_year:
        @param length: An object of the time class that describes the duration of the video.
        @param tracks_num: An integer describing the number of songs on this album.
        @param artist_items: A list of ArtistItem objects.
        @param args: The positional arguments to pass to the constructor of the Item class.
        @param kwargs: The key arguments to pass to the constructor of the Item class.
        """
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.tracks_num = tracks_num
        self.release_year = release_year
        self.artist_items = artist_items

    def __repr__(self) -> str:
        return (
            f"Album{super().__repr__()[:-1]}, "
            f"release_year={self.release_year}, "
            f"artist_items={self.artist_items}, "
            f"length={self.length}, "
            f"tracks_num={self.tracks_num}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        return (
            super().__eq__(__value) 
            and self.length == __value.length
            and self.tracks_num == __value.tracks_num
            and self.release_year == __value.release_year
            and self.artist_items == __value.artist_items
        )

    def __hash__(self) -> int:
        return super().__hash__() ^ hash((self.length, self.tracks_num, self.release_year, self.artist_items))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.ALBUM.value,
            "tracks_num": self.tracks_num,
            "release_year": self.release_year,
            "artist_items": [a.dump() for a in self.artist_items],
            "length": None if self.length is None else {
                "hour": self.length.hour,
                "minute": self.length.minute,
                "second": self.length.second
            }
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.tracks_num = data["tracks_num"]
        self.release_year = data["release_year"]
        self.artist_items = utils.get_items(data["artist_items"])
        self.length = utils.get_length(data["length"])


class EPItem(AlbumItem):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"EP{super().__repr__()}[5:]"

    def dump(self) -> Dict:
        d = super().dump()
        d.update({"type": ItemType.EP.value})
        return d


class RadioItem(Item):
    def __init__(self, video_items: Optional[List[YouTubeVideoItem]] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if video_items is None:
            video_items = []
        self.video_items = video_items

    def __repr__(self) -> str:
        return f"Radio{super().__repr__()[:-1]}, video_items={self.video_items}" "}"

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) and self.video_items == __value.video_items

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.video_items)

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.RADIO.value,
            "video_items": [video.dump() for video in self.video_items]
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.video_items = utils.get_items(data["video_items"])


class YouTubePlaylistItem(Item):
    def __init__(
            self, 
            channel_item: Optional[ChannelItem] = None, 
            videos_num: Optional[int] = None, 
            video_items: Optional[List[YouTubeVideoItem]] = None,
            *args, 
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        if video_items is None:
            video_items = []
        self.videos_num = videos_num
        self.channel_item = channel_item
        self.video_items = video_items

    def __repr__(self) -> str:
        return (
            f"YouTubePlaylist{super().__repr__()[:-1]}, "
            f"videos_num={self.videos_num}, "
            f"video_items={self.video_items}, "
            f"channel_item={self.channel_item}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        return (
            super().__eq__(__value)
            and self.videos_num == __value.videos_num
            and self.video_items == __value.video_items
            and self.channel_item == __value.channel_item
        )

    def __hash__(self) -> int:
        return super().__hash__() ^ hash((self.videos_num, self.video_items, self.channel_item))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.YOUTUBE_PLAYLIST.value,
            "videos_num": self.videos_num,
            "video_items": [video.dump() for video in self.video_items],
            "channel_item": None if self.channel_item is None else self.channel_item.dump()
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.videos_num = data["videos_num"]
        self.channel_item = utils.get_item(data["channel_item"])
        self.video_items = utils.get_items(data["video_items"])


class YouTubeMusicPlaylistItem(AlbumItem):
    def __init__(self, views: Optional[int] = None, *args, **kwargs) -> None:
        """
        Initialize this object with the specified parameters.
        @param views: An integer that describes the number of views of the video.
        @param args: The positional arguments to pass to the constructor of the AlbumItem class.
        @param kwargs: The key arguments to pass to the constructor of the AlbumItem class.
        """
        super().__init__(*args, **kwargs)
        self.views = views

    def __repr__(self) -> str:
        return f"YouTubeMusicPlaylist{super().__repr__()[5:-1]}, views={self.views}" "}"

    def __eq__(self, __value: object) -> bool:
        return (
            super().__eq__(__value)
            and self.length == __value.length
            and self.tracks_num == __value.tracks_num
            and self.release_year == __value.release_year
            and self.artist_items == __value.artist_items
            and self.views == __value.views
        )

    def __hash__(self) -> int:
        return super().__hash__() ^ hash((
            self.length,
            self.tracks_num,
            self.release_year,
            self.artist_items,
            self.views
        ))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.YOUTUBE_MUSIC_PLAYLIST.value,
            "views": self.views
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.views = data["views"]


class SingleItem(AlbumItem):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"Single{super().__repr__()}"

    def dump(self) -> Dict:
        d = super().dump()
        d.update({"type": ItemType.SINGLE.value})
        return d


class SongItem(Item):
    def __init__(
            self,
            length: Optional[time] = None,
            reproductions: Optional[int] = None,
            album_item: Optional[AlbumItem] = None,
            artist_items: Optional[List[ArtistItem]] = None,
            *args,
            **kwargs,
    ) -> None:
        """
        Initialize this object with the specified parameters.
        @param length: An object of the time class that describes the duration of the video.
        @param reproductions: An integer describing the number of plays of this song.
        @param album_item: An AlbumItem object of which this song is a part.
        @param artist_items: A list of ArtistItem objects.
        @param args: The positional arguments to pass to the constructor of the Item class.
        @param kwargs: The key arguments to pass to the constructor of the Item class.
        """
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.reproductions = reproductions
        self.album_item = album_item
        self.artist_items = artist_items

    def __repr__(self) -> str:
        return (
            f"Song{super().__repr__()[:-1]}, "
            f"length={self.length}, "
            f"reproductions={self.reproductions}, "
            f"album_item={self.album_item}, "
            f"artist_items={self.artist_items}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        return (
            super().__eq__(__value)
            and self.length == __value.length
            and self.reproductions == __value.reproductions
            and self.album_item == __value.album_item
            and self.artist_items == __value.artist_items
        )

    def __hash__(self) -> int:
        return super().__hash__() ^ hash((
            self.reproductions,
            self.length,
            self.album_item,
            self.artist_items
        ))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.SONG.value,
            "reproductions": self.reproductions,
            "album_item": None if self.album_item is None else self.album_item.dump(),
            "artist_items": [a.dump() for a in self.artist_items],
            "length": None if self.length is None else {
                "hour": self.length.hour,
                "minute": self.length.minute,
                "second": self.length.second
            }
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.reproductions = data["reproductions"]
        self.artist_items = utils.get_items(data["artist_items"])
        self.album_item = utils.get_item(data["album_item"])
        self.length = utils.get_length(data["length"])


class ProfileItem(Item):
    def __init__(self, handle: Optional[str] = None, *args, **kwargs) -> None:
        """
        Initialize this object with the specified parameters.
        @param handle: A string describing the unique identifier associated with the profile.
        @param args: The positional arguments to pass to the constructor of the Item class.
        @param kwargs: The key arguments to pass to the constructor of the Item class.
        """
        super().__init__(*args, **kwargs)
        self.handle = handle

    def __repr__(self) -> str:
        return f"Profile{super().__repr__()[:-1]}, handle={self.handle}" "}"

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) and self.handle == __value.handle

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.handle)

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.PROFILE.value,
            "handle": self.handle
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.handle = data["handle"]


class PodcastItem(Item):
    def __init__(
            self,
            length: Optional[time] = None,
            artist_items: Optional[List[ArtistItem]] = None,
            *args,
            **kwargs,
    ) -> None:
        """
        Initialize this object with the specified parameters.
        @param length: An object of the time class that describes the duration of the video.
        @parm artist_items: A list of ArtistItem objects.
        @param args: The positional arguments to pass to the constructor of the Item class.
        @param kwargs: The key arguments to pass to the constructor of the Item class.
        """
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.artist_items = artist_items

    def __repr__(self):
        return f"Podcast{super().__repr__()[:-1]}, length={self.length}, artist_items={self.artist_items}" "}"

    def __eq__(self, __value: object) -> bool:
        return (
            super().__eq__(__value) 
            and self.length == __value.length 
            and self.artist_items == __value.artist_items
        )

    def __hash__(self) -> int:
        return super().__hash__() ^ hash((self.length, self.artist_items))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.PODCAST.value,
            "artist_items": [a.dump for a in self.artist_items],
            "length": None if self.length is None else {
                "hour": self.length.hour,
                "minute": self.length.minute,
                "second": self.length.second
            }
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.artist_items = utils.get_items(data["artist_items"])
        self.length = utils.get_length(data["length"])


class EpisodeItem(Item):
    def __init__(
            self,
            publication_date: Optional[date] = None,
            length: Optional[time] = None,
            artist_items: Optional[List[ArtistItem]] = None,
            *args,
            **kwargs,
    ) -> None:
        """
        Initialize this object with the specified parameters.
        @param publication_date: An object of the date class that describes the publication date of this episode.
        @param length: An object of the time class that describes the duration of the video.
        @param artist_items: A list of ArtistItem objects.
        @param args: The positional arguments to pass to the constructor of the Item class.
        @param kwargs: The key arguments to pass to the constructor of the Item class.
        """
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.publication_date = publication_date
        self.artist_items = artist_items

    def __repr__(self):
        return (
            f"Episode{super().__repr__()[:-1]}, "
            f"publication_date={self.publication_date}, "
            f"length={self.length}, "
            f"artist_items={self.artist_items}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        return (
            super().__eq__(__value)
            and self.length == __value.length
            and self.artist_items == __value.artist_items
            and self.publication_date == __value.publication_date
        )

    def __hash__(self) -> int:
        return super().__hash__() ^ hash((self.length, self.artist_items, self.publication_date))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.EPISODE.value,
            "artist_items": [a.dump() for a in self.artist_items],
            "publication_date": None if self.publication_date is None else {
                "month": self.publication_date.month,
                "day": self.publication_date.day,
                "year": self.publication_date.year
            },
            "length": None if self.length is None else {
                "hour": self.length.hour,
                "minute": self.length.minute,
                "second": self.length.second
            }
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.artist_items = utils.get_items(data["artist_items"])
        self.publication_date = utils.get_publication_date(data["publication_date"])
        self.length = utils.get_length(data["length"])
