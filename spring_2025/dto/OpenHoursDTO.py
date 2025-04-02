from dataclasses import dataclass


@dataclass
class OpenHours:
    day: str
    open_time: str
    close_time: str
