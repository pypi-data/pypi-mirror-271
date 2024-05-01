from enum import Enum
from threading import Event

class PriorityOrder(Enum):
    Low = 0
    Normal = 1
    High = 2


class EventType(Enum):
    LINE = 0
    CHAR = 1

class EventWithType(Event):
    def __init__(self, type: EventType) -> None:
        self.type = type
        super().__init__()
