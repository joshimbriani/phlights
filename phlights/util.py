from datetime import date, timedelta
from copy import deepcopy

from phlights.constants import API_BASE, Day
from phlights.errors.configuration_error import ConfigurationError

def build_flight_search_queries(flight_search_builder):
    queries = []

    query_string = ["partner=picky", "max_stopovers=0"]

    # build the rest of the string
    query_string.append("fly_from=" + flight_search_builder._from_location)
    query_string.append("fly_to=" + flight_search_builder._to_location)

    if flight_search_builder._departure_time:
        dpt_time_str = flight_search_builder.get_departure_time_string()
        query_string.append("dtime_from=" + dpt_time_str[0])
        query_string.append("dtime_to=" + dpt_time_str[1])

    if flight_search_builder._arrival_time:
        arr_time_str = flight_search_builder.get_arrival_time_string()
        query_string.append("atime_from=" + arr_time_str[0])
        query_string.append("atime_to=" + arr_time_str[1])

    if flight_search_builder._return_departure_time:
        ret_dpt_time_str = flight_search_builder.get_return_departure_time_string()
        query_string.append("ret_dtime_from=" + ret_dpt_time_str[0])
        query_string.append("ret_dtime_to=" + ret_dpt_time_str[1])

    if flight_search_builder._return_arrival_time:
        ret_arr_time_str = flight_search_builder.get_return_arrival_time_string()
        query_string.append("ret_atime_from=" + ret_arr_time_str[0])
        query_string.append("ret_atime_to=" + ret_arr_time_str[1])

    # generate dates given the conditions
    date_range = flight_search_builder.get_date_range()
    dates = generate_dates_meeting_conditions(date_range[0], flight_search_builder._departure_day.value, flight_search_builder._return_arrival_day.value, date_range[1])

    # splice the dates into the queries
    for start_end_pair in dates:
        query_copy = deepcopy(query_string)
        query_copy.append("date_from=" + start_end_pair[0].strftime("%d/%m/%Y"))
        query_copy.append("date_to=" + start_end_pair[0].strftime("%d/%m/%Y"))
        query_copy.append("ret_date_from=" + start_end_pair[1].strftime("%d/%m/%Y"))
        query_copy.append("ret_date_to=" + start_end_pair[1].strftime("%d/%m/%Y"))
        query_copy.append("nights_in_dst_from=" + str((start_end_pair[1] - start_end_pair[0]).days - 1))
        query_copy.append("nights_in_dst_to=" + str((start_end_pair[1] - start_end_pair[0]).days))
        queries.append(API_BASE + "&".join(query_copy))

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
