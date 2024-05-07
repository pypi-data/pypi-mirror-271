from enum import Enum


class EventType(Enum):
    """Enum of currently supported event_types"""

    DATA = "data"
    STATE = "state"
    CONFIG = "config"
    CMD = "cmd"
