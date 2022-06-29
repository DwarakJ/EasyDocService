from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class NoteType(Enum):
    TECH = 1
    KT = 2
    MOM = 3
    IDEAS = 4
    TODO = 5

@dataclass
class Notes:
    id: int
    name: str
    note: str
    created_time: datetime
    modified_time: datetime
    note_type: NoteType





