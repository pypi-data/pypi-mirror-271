from dataclasses import dataclass
from typing import Optional, Dict
from innertube_de.types import EndpointType


@dataclass(kw_only=True)
class Endpoint:
    params: Optional[str] = None

    def dump(self) -> Dict:
        return {"params": self.params}

    def load(self, data: Dict) -> None:
        self.params = data["params"]


@dataclass(kw_only=True)
class BrowseEndpoint(Endpoint):
    browse_id: Optional[str] = None

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


@dataclass(kw_only=True)
class YouTubeBrowseEndpoint(BrowseEndpoint):
    canonical_base_url: Optional[str] = None

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


@dataclass(kw_only=True)
class SearchEndpoint(Endpoint):
    query: Optional[str] = None

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


@dataclass(kw_only=True)
class WatchEndpoint(Endpoint):
    video_id: Optional[str] = None
    playlist_id: Optional[str] = None
    index: Optional[int] = None

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


@dataclass(kw_only=True)
class ContinuationEndpoint(Endpoint):
    continuation: Optional[str] = None

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


@dataclass(kw_only=True)
class UrlEndpoint(Endpoint):
    url: Optional[str] = None

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
