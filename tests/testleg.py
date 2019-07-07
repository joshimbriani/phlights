import unittest
from datetime import datetime

import pytz
from tzlocal import get_localzone

from phlights.models.leg import Leg
from phlights.models.flight import Flight


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

        self.assertEqual(l.layovers, 1)

    def test_duration(self):
        departure_time = datetime(2020, 1, 1, 10, 10, 10)
        departure_time_stamp = departure_time.timestamp()

        arrival_time = datetime(2020, 1, 1, 12, 10, 10)
        arrival_time_stamp = arrival_time.timestamp()

        l = Leg(departure_time=departure_time_stamp, arrival_time=arrival_time_stamp)
        self.assertEqual(l.duration.total_seconds(), 7200)

    def test_to_string(self):
        f1 = Flight(from_location="San Francisco", to_location="Orlando", from_location_code="SFO", to_location_code="MCO", departure_time=datetime(2020, 1, 1, 10, 10, 10).timestamp(), arrival_time=datetime(2020, 1, 1, 12, 10, 10).timestamp(), airline="UA", flight_number=1120)
        f2 = Flight(from_location="Orlando", to_location="Columbus", from_location_code="MCO", to_location_code="CMH", departure_time=datetime(2020, 1, 1, 12, 10, 10).timestamp(), arrival_time=datetime(2020, 1, 1, 14, 10, 10).timestamp(), airline="UA", flight_number=1121)
        l = Leg(from_location="San Francisco", to_location="Orlando", from_location_code="SFO", to_location_code="MCO", departure_time=datetime(2020, 1, 1, 10, 10, 10).timestamp(), arrival_time=datetime(2020, 1, 1, 14, 10, 10).timestamp(), flights=[f1, f2])

        s = ""
        s += "Leg from San Francisco to Orlando\n"
        s += "    Duration: 4.0 hours\n"
        s += "    Layovers: 1\n"
        s += "    " + f1.__str__() + "\n"
        s += "    " + f2.__str__() + "\n"
        self.assertEqual(s, l.__str__())
