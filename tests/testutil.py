import unittest
from datetime import datetime, time, date, timedelta

import responses
import requests

from phlights.constants import Day
from phlights.errors.configuration_error import ConfigurationError
from phlights.flightsearchbuilder import FlightSearchBuilder
from phlights.util import (build_flight_search_queries,
                           generate_dates_meeting_conditions,
                           make_api_request,
                           find_route)


class UtilTest(unittest.TestCase):
    def test_build_flight_search_queries_min(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1))

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/03/2020")

    def test_build_flight_search_queries_with_layover(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1), allow_layovers=True)

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=1&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/03/2020")

    def test_build_flight_search_queries_with_departure_time(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1), departure_time=(time(hour=10, minute=0), time(hour=12, minute=0)))

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&dtime_from=10:00&dtime_to=12:00&date_from=01/01/2020&date_to=01/03/2020")

    def test_build_flight_search_queries_with_arrival_time(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1), arrival_time=(time(hour=10, minute=0), time(hour=12, minute=0)))

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&atime_from=10:00&atime_to=12:00&date_from=01/01/2020&date_to=01/03/2020")
    
    def test_build_flight_search_queries_with_return_departure_time(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1), return_departure_time=(time(hour=10, minute=0), time(hour=12, minute=0)))

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&ret_dtime_from=10:00&ret_dtime_to=12:00&date_from=01/01/2020&date_to=01/03/2020")

    def test_build_flight_search_queries_with_return_arrival_time(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1), return_arrival_time=(time(hour=10, minute=0), time(hour=12, minute=0)))

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&ret_atime_from=10:00&ret_atime_to=12:00&date_from=01/01/2020&date_to=01/03/2020")

    def test_build_flight_search_queries_with_departure_day(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1), departure_day=Day.MONDAY)

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/03/2020")

    def test_build_flight_search_queries_with_return_arrival_day(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1), return_arrival_day=Day.MONDAY)

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/03/2020")

    def test_build_flight_search_queries_with_departure_day_and_return_arrival_day(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1), departure_day=Day.SATURDAY, return_arrival_day=Day.MONDAY)

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 9)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=04/01/2020&date_to=04/01/2020&return_from=06/01/2020&return_to=06/01/2020&nights_in_dst_from=1&nights_in_dst_to=1")
        self.assertEqual(query[1], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=11/01/2020&date_to=11/01/2020&return_from=13/01/2020&return_to=13/01/2020&nights_in_dst_from=1&nights_in_dst_to=1")
        self.assertEqual(query[2], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=18/01/2020&date_to=18/01/2020&return_from=20/01/2020&return_to=20/01/2020&nights_in_dst_from=1&nights_in_dst_to=1")
        self.assertEqual(query[3], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=25/01/2020&date_to=25/01/2020&return_from=27/01/2020&return_to=27/01/2020&nights_in_dst_from=1&nights_in_dst_to=1")
        self.assertEqual(query[4], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/02/2020&date_to=01/02/2020&return_from=03/02/2020&return_to=03/02/2020&nights_in_dst_from=1&nights_in_dst_to=1")
        self.assertEqual(query[5], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=08/02/2020&date_to=08/02/2020&return_from=10/02/2020&return_to=10/02/2020&nights_in_dst_from=1&nights_in_dst_to=1")
        self.assertEqual(query[6], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=15/02/2020&date_to=15/02/2020&return_from=17/02/2020&return_to=17/02/2020&nights_in_dst_from=1&nights_in_dst_to=1")
        self.assertEqual(query[7], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=22/02/2020&date_to=22/02/2020&return_from=24/02/2020&return_to=24/02/2020&nights_in_dst_from=1&nights_in_dst_to=1")
        self.assertEqual(query[8], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=29/02/2020&date_to=29/02/2020&return_from=02/03/2020&return_to=02/03/2020&nights_in_dst_from=1&nights_in_dst_to=1")

    def test_build_flight_search_queries_with_departure_date(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1), departure_date=date(2020, 1, 1))

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/03/2020")

    def test_build_flight_search_queries_with_return_departure_date(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1), return_departure_date=date(2020, 1, 1))

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/03/2020")

    def test_build_flight_search_queries_with_departure_date_and_return_departure_date(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1), departure_date=date(2020, 1, 1), return_departure_date=date(2020, 2, 2))

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/01/2020&return_from=02/02/2020&return_to=02/02/2020")

    def test_generate_dates_meeting_conditions(self):
        start_date = date(year=2020,month=1,day=1)
        end_date = date(year=2020, month=3, day=1)

        departure_day = Day.SATURDAY
        return_departure_day = Day.MONDAY

        dates = generate_dates_meeting_conditions(start_date, departure_day.value, return_departure_day.value, end_date)
        self.assertEqual(len(dates), 9)
        self.assertEqual(dates[0], (date(2020, 1, 4), date(2020,1,6)))
        self.assertEqual(dates[1], (date(2020, 1, 11), date(2020,1,13)))
        self.assertEqual(dates[2], (date(2020, 1, 18), date(2020,1,20)))
        self.assertEqual(dates[3], (date(2020, 1, 25), date(2020,1,27)))
        self.assertEqual(dates[4], (date(2020, 2, 1), date(2020,2,3)))
        self.assertEqual(dates[5], (date(2020, 2, 8), date(2020,2,10)))
        self.assertEqual(dates[6], (date(2020, 2, 15), date(2020,2,17)))
        self.assertEqual(dates[7], (date(2020, 2, 22), date(2020,2,24)))
        self.assertEqual(dates[8], (date(2020, 2, 29), date(2020,3,2)))

    def test_generate_dates_meeting_conditions_bad_start_date(self):
        start_date = datetime(year=2020,month=1,day=1)
        end_date = date(year=2020, month=3, day=1)

        departure_day = Day.SATURDAY
        return_departure_day = Day.MONDAY

        dates = generate_dates_meeting_conditions(start_date, departure_day.value, return_departure_day.value, end_date)
        self.assertIsInstance(dates, ConfigurationError)

    def test_generate_dates_meeting_conditions_bad_end_day(self):
        start_date = date(year=2020,month=1,day=1)
        end_date = datetime(year=2020, month=3, day=1)

        departure_day = Day.SATURDAY
        return_departure_day = Day.MONDAY

        dates = generate_dates_meeting_conditions(start_date, departure_day.value, return_departure_day.value, end_date)
        self.assertIsInstance(dates, ConfigurationError)

    def test_generate_dates_meeting_conditions_bad_departure_day(self):
        start_date = date(year=2020,month=1,day=1)
        end_date = date(year=2020, month=3, day=1)

        departure_day = "Sa"
        return_departure_day = Day.MONDAY

        dates = generate_dates_meeting_conditions(start_date, departure_day, return_departure_day, end_date)
        self.assertIsInstance(dates, ConfigurationError)

    def test_generate_dates_meeting_conditions_bad_return_departure_day(self):
        start_date = date(year=2020,month=1,day=1)
        end_date = date(year=2020, month=3, day=1)

        departure_day = Day.SATURDAY
        return_departure_day = "Mo"

        dates = generate_dates_meeting_conditions(start_date, departure_day, return_departure_day, end_date)
        self.assertIsInstance(dates, ConfigurationError)

    @responses.activate
    def test_make_api_request(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1))

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/03/2020")
        
        responses.add(responses.GET, 'https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/03/2020', json={'data': []}, status=200)

        r = make_api_request(query[0])

        self.assertIsNotNone(r)

    @responses.activate
    def test_make_api_request_bad_response_code(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1))

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/03/2020")
        
        responses.add(responses.GET, 'https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/03/2020', json={}, status=400)

        r = make_api_request(query[0])

        self.assertIsNone(r)

    @responses.activate
    def test_make_api_request_bad_response_body(self):
        f = FlightSearchBuilder(from_location="SFO", to_location="MCO", start_from=date(2020, 1, 1))

        query = build_flight_search_queries(f)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0], "https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/03/2020")
        
        responses.add(responses.GET, 'https://api.skypicker.com/flights?partner=picky&curr=USD&max_stopovers=0&fly_from=SFO&fly_to=MCO&date_from=01/01/2020&date_to=01/03/2020', json={'error': 'bad_response'}, status=200)

        r = make_api_request(query[0])

        self.assertIsNone(r)

    def test_find_route(self):
        flight_data = [
            {"flyFrom": "SFO", "flyTo": "MCO"},
            {"flyFrom": "MCO", "flyTo": "CMH"}
        ]

        start = "SFO"
        end = "CMH"

        route = find_route(flight_data, start, end)

        self.assertIsNotNone(route)
        self.assertEqual(len(route), 2)
        self.assertEqual(route[0], {"flyFrom": "SFO", "flyTo": "MCO"})
        self.assertEqual(route[1], {"flyFrom": "MCO", "flyTo": "CMH"})

    def test_find_route_no_route(self):
        flight_data = [
            {"flyFrom": "SFO", "flyTo": "MCO"},
            {"flyFrom": "MCO", "flyTo": "CMH"}
        ]

        start = "MCO"
        end = "SFO"

        route = find_route(flight_data, start, end)

        self.assertIsNone(route)

    def test_find_route_single_route(self):
        flight_data = [
            {"flyFrom": "SFO", "flyTo": "MCO"},
            {"flyFrom": "MCO", "flyTo": "CMH"}
        ]

        start = "SFO"
        end = "MCO"

        route = find_route(flight_data, start, end)

        self.assertIsNotNone(route)
        self.assertEqual(len(route), 1)
        self.assertEqual(route[0], {"flyFrom": "SFO", "flyTo": "MCO"})