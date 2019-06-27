from datetime import date, timedelta

from pyflightsearch.constants import API_BASE
from pyflightsearch.errors.configuration_error import ConfigurationError

def build_flight_search_queries(flight_search_builder):
    queries = []

    return API_BASE

def generate_dates_meeting_conditions(start_date, departure_day, return_day, lookahead_weeks):
    if not isinstance(start_date, date):
        return ConfigurationError("start_date input to generate_dates_meeting_conditions must be a date object")
    if type(departure_day) != int:
        return ConfigurationError("departure_day input to generate_dates_meeting_conditions must be a int")
    if type(return_day) != int:
        return ConfigurationError("return_day input to generate_dates_meeting_conditions must be a int")
    if type(lookahead_weeks) != int:
        return ConfigurationError("lookahead_weeks input to generate_dates_meeting_conditions must be a int")

    pairs = []
    start = None
    for day in daterange(start_date, lookahead_weeks * 7 + 6):
        if day.weekday() == departure_day:
            start = day

        if start and day != start and day.weekday() == return_day:
            pairs.append((start, day))
            start = None

    return pairs

def daterange(start_date, duration):
    for i in range(duration):
        yield start_date + timedelta(i)
