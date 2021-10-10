import builtins
from dataclasses import dataclass
from typing import List
from datetime import datetime

#TODO: Docs

@dataclass
class Lecture:
    start: datetime
    end: datetime
    subject: str
    group: str = None
    building: str = None
    room: str = None
    lecture_type: str = None
    lecturer: str = None
    title: str = None

@dataclass
class TimeOff:
    start: datetime
    end: datetime

@dataclass
class Timetable:
    lectures: List[Lecture]
    days_off: List[TimeOff]
    buildings: List[str]

