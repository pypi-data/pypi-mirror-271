from typing import Optional
from typing import Dict


class StreamData:
    def __init__(
            self,
            *,
            stream_type: Optional[str] = None,
            subtype: Optional[str] = None,
            video_codec: Optional[str] = None,
            audio_codec: Optional[str] = None,
            resolution: Optional[str] = None,
            audio_sample_rate: Optional[int] = None,
            bitrate: Optional[int] = None,
            average_bitrare: Optional[int] = None,
            fps: Optional[int] = None,
            signature_cipher: Optional[str] = None,
            file_size: Optional[int] = None
    ) -> None:
        self.stream_type = stream_type
        self.subtype = subtype
        self.video_codec = video_codec
        self.audio_codec = audio_codec
        self.resolution = resolution
        self.audio_sample_rate = audio_sample_rate
        self.bitrate = bitrate
        self.average_bitrate = average_bitrare
        self.fps = fps
        self.signature_cipher = signature_cipher
        self.file_size = file_size

    def __repr__(self) -> str:
        return (
            "StreamData{"
            f"stream_type={self.stream_type}, "
            f"subtype={self.subtype}, "
            f"video_codec={self.video_codec}, "
            f"audio_codec={self.audio_codec}, "
            f"resolution={self.resolution}, "
            f"audio_sample_rate={self.audio_sample_rate}, "
            f"bitrate={self.bitrate}, "
            f"average_bitrate={self.average_bitrate}, "
            f"fps={self.fps}, "
            f"signature_cipher={self.signature_cipher}, "
            f"file_size={self.file_size}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, StreamData):
            return (
                self.stream_type == __value.stream_type
                and self.subtype == __value.subtype
                and self.video_codec == __value.video_codec
                and self.audio_codec == __value.audio_codec
                and self.resolution == __value.resolution
                and self.audio_sample_rate == __value.audio_sample_rate
                and self.bitrate == __value.bitrate
                and self.average_bitrate == __value.average_bitrate
                and self.fps == __value.fps
                and self.signature_cipher == __value.signature_cipher
                and self.file_size == __value.file_size
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((
            self.stream_type,
            self.subtype,
            self.video_codec,
            self.audio_codec,
            self.resolution,
            self.audio_sample_rate,
            self.bitrate,
            self.average_bitrate,
            self.fps,
            self.signature_cipher,
            self.file_size
        ))

    def dump(self) -> Dict:
        return {
            "stream_type": self.stream_type,
            "subtype": self.subtype,
            "video_codec": self.video_codec,
            "audio_codec": self.audio_codec,
            "resolution": self.resolution,
            "audio_sample_rate": self.audio_sample_rate,
            "bitrate": self.bitrate,
            "average_bitrare": self.average_bitrate,
            "fps": self.fps,
            "signature_cipher": self.signature_cipher,
            "file_size": self.file_size
        }

    def load(self, data: Dict) -> None:
        self.stream_type = data["stream_type"]
        self.subtype = data["subtype"]
        self.video_codec = data["video_codec"]
        self.audio_codec = data["audio_codec"]
        self.resolution = data["resolution"]
        self.audio_sample_rate = data["audio_sample_rate"]
        self.bitrate = data["bitrate"]
        self.average_bitrate = data["average_bitrate"]
        self.fps = data["fps"]
        self.signature_cipher = data["signature_cipher"]
        self.file_size = data["file_size"]
