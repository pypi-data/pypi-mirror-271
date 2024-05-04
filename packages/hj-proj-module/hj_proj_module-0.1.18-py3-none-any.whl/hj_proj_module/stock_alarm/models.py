import orjson
import base64
from dataclasses import dataclass, asdict
from enum import Enum, auto, Flag


@dataclass
class StockAnalysisEvent:
    symbol: str
    start: str
    end: str
    email: str

    @property
    def get_key(self):
        return f"{self.symbol}_{self.start}_{self.end}"


@dataclass
class NotificationEvent:
    class Types(Flag):
        EMAIL = auto()
        SMS = auto()
        TELEGRAM = auto()

    user_id: str
    title: str
    msg: str
    type: Types

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            user_id=d["user_id"],
            title=d["title"],
            msg=d["msg"],
            type=cls.Types(d["type"]),
        )

    @classmethod
    def from_base64_str(cls, s: str):
        base64_decoded_bytes: bytes = base64.b64decode(s)
        d: dict = orjson.loads(base64_decoded_bytes)
        return cls(
            user_id=d["user_id"],
            title=d["title"],
            msg=d["msg"],
            type=cls.Types(d["type"]),
        )

    def to_bytes(self) -> bytes:
        return orjson.dumps(asdict(self), option=orjson.OPT_NAIVE_UTC)
