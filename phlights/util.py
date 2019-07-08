from datetime import date, timedelta, datetime
from copy import deepcopy

import requests

from phlights.constants import API_BASE, Day
from phlights.errors.configuration_error import ConfigurationError

def build_flight_search_queries(flight_search_builder):
    queries = []

    query_string = ["partner=picky", "curr=USD"]

    query_string.append("max_stopovers=" + ("1" if flight_search_builder._allow_layovers else "0"))

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
    if flight_search_builder._departure_day and flight_search_builder._return_arrival_day:
        dates = generate_dates_meeting_conditions(date_range[0], flight_search_builder._departure_day.value, flight_search_builder._return_arrival_day.value, date_range[1])
        for start_end_pair in dates:
            query_copy = deepcopy(query_string)
            query_copy.append("date_from=" + start_end_pair[0].strftime("%d/%m/%Y"))
            query_copy.append("date_to=" + start_end_pair[0].strftime("%d/%m/%Y"))
            query_copy.append("return_from=" + start_end_pair[1].strftime("%d/%m/%Y"))
            query_copy.append("return_to=" + start_end_pair[1].strftime("%d/%m/%Y"))
            query_copy.append("nights_in_dst_from=" + str((start_end_pair[1] - start_end_pair[0]).days - 1))
            query_copy.append("nights_in_dst_to=" + str((start_end_pair[1] - start_end_pair[0]).days - 1))
            queries.append(API_BASE + "&".join(query_copy))
    elif flight_search_builder._departure_date and flight_search_builder._return_departure_date:
        # User has specified a firm start and end date
        query_string.append("date_from=" + flight_search_builder._departure_date.strftime("%d/%m/%Y"))
        query_string.append("date_to=" + flight_search_builder._departure_date.strftime("%d/%m/%Y"))
        query_string.append("return_from=" + flight_search_builder._return_departure_date.strftime("%d/%m/%Y"))
        query_string.append("return_to=" + flight_search_builder._return_departure_date.strftime("%d/%m/%Y"))
        queries.append(API_BASE + "&".join(query_string))
    else:
        # User hasn't give a start or end date, instead just set the search start date to start_from
        query_string.append("date_from=" + date_range[0].strftime("%d/%m/%Y"))
        query_string.append("date_to=" + date_range[1].strftime("%d/%m/%Y"))
        queries.append(API_BASE + "&".join(query_string))

    # return the queries
    return queries

def generate_dates_meeting_conditions(start_date, departure_day, return_day, stop_date):
    if not isinstance(start_date, date) or isinstance(start_date, datetime):
        return ConfigurationError("start_date input to generate_dates_meeting_conditions must be a date object")
    if type(departure_day) != int:
        return ConfigurationError("departure_day input to generate_dates_meeting_conditions must be a int")
    if type(return_day) != int:
        return ConfigurationError("return_day input to generate_dates_meeting_conditions must be a int")
    if not isinstance(stop_date, date) or isinstance(stop_date, datetime):
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

def make_api_request(query_string):
    r = requests.get(query_string)
    if r.status_code != 200 and r.status_code != 201:
        return None
    response_json = r.json()
    if "data" not in response_json:
        return None
    return response_json["data"]

def find_route(flight_data, start, end):
    return find_route_helper(flight_data, start, end, set())

def find_route_helper(flight_data, start, end, seen):
    for route in flight_data:
        if (route["flyFrom"], route["flyTo"]) in seen:
            continue
        if route["flyFrom"] == start and route["flyTo"] == end:
            return [route]
        elif route["flyFrom"] == start:
            seen_clone = deepcopy(seen)
            seen_clone.add((route["flyFrom"], route["flyTo"]))
            rest_of_path = find_route_helper(flight_data, route["flyTo"], end, seen_clone)
            if rest_of_path:
                return [route] + rest_of_path
    return None