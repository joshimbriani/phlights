from enum import Enum

API_BASE = 'https://api.skypicker.com/flights?'
DEFAULT_REQUEST_DELAY = 3
MAX_LOOKAHEAD_WEEKS = 12

class Day(Enum):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6