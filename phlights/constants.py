from enum import Enum

API_BASE = 'https://api.skypicker.com/flights?'
DEFAULT_REQUEST_DELAY = 3
MAX_LOOKAHEAD_WEEKS = 12
MAX_LOOKAHEAD_DAYS = 60
API_BACKOFF_SECONDS = 5

class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6