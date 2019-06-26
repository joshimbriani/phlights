from datetime import date, timedelta

from pyflightsearch.constants import API_BASE

def build_flight_search_queries(flight_search_builder):
    queries = []

    return API_BASE

def generate_dates_meeting_conditions(start_date, departure_day, return_day, lookahead_weeks):
    start_end_pair = []
    if not isinstance(start_date, date):
        pass

def daterange(start_date, duration):
    for i in range(duration):
        yield start_date + timedelta(i)