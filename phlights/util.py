from datetime import date, timedelta

from phlights.constants import API_BASE, Day
from phlights.errors.configuration_error import ConfigurationError

def build_flight_search_queries(flight_search_builder):
    queries = []

    query_string = []

    # build the rest of the string
    query_string.append("fly_from=" + flight_search_builder.from_location)
    query_string.append("fly_to=" + flight_search_builder.to_location)

    query_string.append("date_from=" + flight_search_builder.get_date_range_string()[0])
    query_string.append("date_to=" + flight_search_builder.get_date_range_string()[1])

    if flight_search_builder.departure_time:
        dpt_time_str = flight_search_builder.get_departure_time_string()
        query_string.append("dtime_from=" + dpt_time_str[0])
        query_string.append("dtime_to=" + dpt_time_str[1])

    if flight_search_builder.arrival_time:
        arr_time_str = flight_search_builder.get_arrival_time_string()
        query_string.append("atime_from=" + dpt_time_str[0])
        query_string.append("atime_to=" + dpt_time_str[1])

    if flight_search_builder.return_departure_time:
        ret_dpt_time_str = flight_search_builder.get_return_departure_time_string()
        query_string.append("ret_dtime_from=" + ret_dpt_time_str[0])
        query_string.append("ret_dtime_to=" + ret_dpt_time_str[1])

    if flight_search_builder.return_arrival_time:
        ret_arr_time_str = flight_search_builder.get_return_arrival_time_string()
        query_string.append("ret_atime_from=" + ret_arr_time_str[0])
        query_string.append("ret_atime_to=" + ret_arr_time_str[1])

    return query_string

    # generate dates given the conditions
    search_dates  = flight_search_builder.get_date_range_string()
    dates = generate_dates_meeting_conditions(search_dates[0], flight_search_builder.departure_day, flight_search_builder.return_day, search_dates[1])

    # splice the dates into the queries

    # return the queries
    return queries

def generate_dates_meeting_conditions(start_date, departure_day, return_day, stop_date):
    if not isinstance(start_date, date):
        return ConfigurationError("start_date input to generate_dates_meeting_conditions must be a date object")
    if type(departure_day) != int:
        return ConfigurationError("departure_day input to generate_dates_meeting_conditions must be a int")
    if type(return_day) != int:
        return ConfigurationError("return_day input to generate_dates_meeting_conditions must be a int")
    if not isinstance(stop_date, date):
        return ConfigurationError("stop_date input to generate_dates_meeting_conditions must be a date object")

    pairs = []
    start = None
    for day in daterange(start_date, ((stop_date - start_date).days) + 6):
        if day.weekday() == departure_day:
            start = day

        if start and day != start and day.weekday() == return_day:
            pairs.append((start, day))
            start = None

    return pairs

def daterange(start_date, duration):
    for i in range(duration):
        yield start_date + timedelta(i)
