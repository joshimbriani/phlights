import unittest
from datetime import datetime

import pytz
from tzlocal import get_localzone

from phlights.models.leg import Leg


class LegTest(unittest.TestCase):
    def test_empty_leg(self):
        l = Leg()

        self.assertEqual(l.departure_time, datetime(1970,1,1))
        self.assertEqual(l.arrival_time, datetime(1970,1,1))
        self.assertEqual(l.flights, [])
        self.assertEqual(l.from_location, "")
        self.assertEqual(l.from_location_code, "")
        self.assertEqual(l.to_location, "")
        self.assertEqual(l.to_location_code, "")
        self.assertEqual(l.duration, 0)
        self.assertEqual(l.layovers, -1)

    def test_from_location(self):
        l = Leg(from_location="San Francisco")

        self.assertEqual(l.from_location, "San Francisco")

    def test_from_location_code(self):
        l = Leg(from_location_code="SFO")

        self.assertEqual(l.from_location_code, "SFO")

    def test_to_location(self):
        l = Leg(to_location="Orlando")

        self.assertEqual(l.to_location, "Orlando")

    def test_to_location_code(self):
        l = Leg(to_location_code="MCO")

        self.assertEqual(l.to_location_code, "MCO")

    def test_flights(self):
        l = Leg(flights=[{"flight_number": 1}, {"flight_number": 2}])

        self.assertEqual(len(l.flights), 2)
        self.assertEqual(l.flights[0]["flight_number"], 1)
        self.assertEqual(l.flights[1]["flight_number"], 2)

    def test_departure_time(self):
        departure_time = datetime(2020, 1, 1, 10, 10, 10).replace(tzinfo=pytz.UTC)
        departure_time_stamp = departure_time.timestamp()
        l = Leg(departure_time=departure_time_stamp)
        self.assertEqual(l.departure_time, departure_time)

    def test_arrival_time(self):
        arrival_time = datetime(2020, 1, 1, 10, 10, 10).replace(tzinfo=pytz.UTC)
        arrival_time_stamp = arrival_time.timestamp()
        l = Leg(arrival_time=arrival_time_stamp)
        self.assertEqual(l.arrival_time, arrival_time)

    def test_layovers(self):
        l = Leg(flights=[{"flight_number": 1}, {"flight_number": 2}])

        self.assertEquals(l.layovers, 1)

    def test_duration(self):
        departure_time = datetime(2020, 1, 1, 10, 10, 10)
        departure_time_stamp = departure_time.timestamp()

        arrival_time = datetime(2020, 1, 1, 12, 10, 10)
        arrival_time_stamp = arrival_time.timestamp()

        l = Leg(departure_time=departure_time_stamp, arrival_time=arrival_time_stamp)
        self.assertEqual(l.duration.total_seconds(), 7200)