from typing import Optional
from typing import Dict
from innertube_de.types import EndpointType


class Endpoint:
    def __init__(
            self,
            params: Optional[str] = None
    ) -> None:
        """
        Initialize this object with the specified parameters.
        @param params: Parameters associated with the endpoint.
        """
        self.params = params

    def __repr__(self) -> str:
        return "Endpoint{" f"params={self.params}" "}"

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, type(self)) and self.params == __value.params

    def __hash__(self) -> int:
        return hash((self.params, type(self)))

    def dump(self) -> Dict:
        """
        Serialize this object.
        @return: A dictionary that describes the state of this object.
        """
        return {"params": self.params}

    def load(self, data: Dict) -> None:
        """
        Deserialize this object with the specified dictionary.
        @param data: The dictionary containing the data.
        @return: None
        """
        self.params = data["params"]


class BrowseEndpoint(Endpoint):
    def __init__(self, browse_id: Optional[str] = None, *args, **kwargs) -> None:
        """
        Initialize this object with the specified parameters.
        @param browse_id:
        @param args: The positional arguments to pass to the constructor of the Endpoint class.
        @param kwargs: The key arguments to pass to the constructor of the Endpoint class.
        """
        super().__init__(*args, **kwargs)
        self.browse_id = browse_id

    def __repr__(self) -> str:
        return f"Browse{super().__repr__()[:-1]}, browse_id={self.browse_id}" "}"

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) and self.browse_id == __value.browse_id

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.browse_id)

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": EndpointType.BROWSE.value,
            "browse_id": self.browse_id
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.browse_id = data["browse_id"]


class YouTubeBrowseEndpoint(BrowseEndpoint):
    def __init__(self, canonical_base_url: Optional[str] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.canonical_base_url = canonical_base_url

    def __repr__(self) -> str:
        return f"YouTube{super().__repr__()[:-1]}, canonical_base_url={self.canonical_base_url}" "}"

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) and self.canonical_base_url == __value.canonical_base_url

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.canonical_base_url)

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": EndpointType.YOUTUBE_BROWSE.value,
            "canonical_base_url": self.canonical_base_url
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.canonical_base_url = data["canonical_base_url"]


class SearchEndpoint(Endpoint):
    def __init__(self, query: Optional[str] = None, *args, **kwargs) -> None:
        """
        Initialize this object with the specified parameters.
        @param query: The string object representing the query.
        @param args: The positional arguments to pass to the constructor of the Endpoint class.
        @param kwargs: The key arguments to pass to the constructor of the Endpoint class.
        """
        super().__init__(*args, **kwargs)
        self.query = query

    def __repr__(self) -> str:
        return f"Search{super().__repr__()[:-1]}, query={self.query}" "}"

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) and self.query == __value.query

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.query)

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": EndpointType.SEARCH.value,
            "query": self.query
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.query = data["query"]


class WatchEndpoint(Endpoint):
    def __init__(
            self,
            video_id: Optional[str] = None,
            playlist_id: Optional[str] = None,
            index: Optional[int] = None,
            *args,
            **kwargs,
    ) -> None:
        """
        Initialize this object with the specified parameters.
        @param video_id: The video ID.
        @param playlist_id: The playlist ID.
        @param index: An integer (I don't know what it's for)
        @param args: The positional arguments to pass to the constructor of the Endpoint class.
        @param kwargs: The key arguments to pass to the constructor of the Endpoint class.
        """
        super().__init__(*args, **kwargs)
        self.video_id = video_id
        self.index = index
        self.playlist_id = playlist_id

    def __repr__(self) -> str:
        return (
            f"Watch{super().__repr__()[:-1]}, " 
            f"video_id={self.video_id}, "
            f"playlist_id={self.playlist_id}, "
            f"index={self.index}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        return (
            super().__eq__(__value)
            and self.index == __value.index
            and self.video_id == __value.video_id
            and self.playlist_id == __value.playlist_id
        )

    def __hash__(self) -> int:
        return super().__hash__() ^ hash((self.video_id, self.playlist_id, self.index))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": EndpointType.WATCH.value,
            "video_id": self.video_id,
            "playlist_id": self.playlist_id,
            "index": self.index
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.video_id = data["video_id"]
        self.playlist_id = data["playlist_id"]
        self.index = data["index"]


class ContinuationEndpoint(Endpoint):
    def __init__(self, continuation: Optional[str] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.continuation = continuation

    def __repr__(self) -> str:
        return f"Continuation{super().__repr__()[:-1]}, continuation={self.continuation}" "}"

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) and self.continuation == __value.continuation

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.continuation)

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": EndpointType.CONTINUATION.value,
            "continuation": self.continuation
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.continuation = data["continuation"]


class UrlEndpoint(Endpoint):
    def __init__(self, url: Optional[str] = None, *args, **kwargs) -> None:
        """
        Initialize this object with the specified parameters.
        @param url: A URL (uniform resource locator).
        @param args: The positional arguments to pass to the constructor of the Endpoint class.
        @param kwargs: The key arguments to pass to the constructor of the Endpoint class.
        """
        super().__init__(*args, **kwargs)
        self.url = url

    def __repr__(self) -> str:
        return f"Url{super().__repr__()[:-1]}, url={self.url}" "}"

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) and self.url == __value.url

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.url)

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": EndpointType.URL.value,
            "url": self.url
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.url = data["url"]
