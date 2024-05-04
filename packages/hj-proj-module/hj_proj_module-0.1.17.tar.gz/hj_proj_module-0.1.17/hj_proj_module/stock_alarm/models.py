from dataclasses import dataclass
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
