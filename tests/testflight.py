import unittest
from datetime import datetime

import pytz
from tzlocal import get_localzone

from phlights.models.flight import Flight

class FlightTest(unittest.TestCase):
    def test_empty_flight(self):
        f = Flight()

        self.assertEqual(f.from_location, "")
        self.assertEqual(f.from_location_code, "")
        self.assertEqual(f.to_location, "")
        self.assertEqual(f.to_location_code, "")
        self.assertEqual(f.departure_time, datetime(1970,1,1))
        self.assertEqual(f.arrival_time, datetime(1970,1,1))
        self.assertEqual(f.airline, "")
        self.assertEqual(f.duration, 0)
        self.assertEqual(f.flight_number, -1)

    def test_from_location(self):
        from_location = "San Francisco"
        f = Flight(from_location=from_location)
        self.assertEqual(f.from_location, from_location)

    def test_from_location_code(self):
        from_location_code = "SFO"
        f = Flight(from_location_code=from_location_code)
        self.assertEqual(f.from_location_code, from_location_code)

    def test_to_location(self):
        to_location = "SFO"
        f = Flight(to_location=to_location)
        self.assertEqual(f.to_location, to_location)

    def test_to_location_code(self):
        to_location_code = "SFO"
        f = Flight(to_location_code=to_location_code)
        self.assertEqual(f.to_location_code, to_location_code)

    def test_departure_time(self):
        departure_time = datetime(2020, 1, 1, 10, 10, 10).replace(tzinfo=pytz.UTC)
        departure_time_stamp = departure_time.timestamp()
        f = Flight(departure_time=departure_time_stamp)
        self.assertEqual(f.departure_time, departure_time)

    def test_arrival_time(self):
        arrival_time = datetime(2020, 1, 1, 10, 10, 10).replace(tzinfo=pytz.UTC)
        arrival_time_stamp = arrival_time.timestamp()
        f = Flight(arrival_time=arrival_time_stamp)
        self.assertEqual(f.arrival_time, arrival_time)

    def test_airline(self):
        airline = "UA"
        f = Flight(airline=airline)
        self.assertEqual(f.airline, airline)

    def test_duration(self):
        departure_time = datetime(2020, 1, 1, 10, 10, 10)
        departure_time_stamp = departure_time.timestamp()

        arrival_time = datetime(2020, 1, 1, 12, 10, 10)
        arrival_time_stamp = arrival_time.timestamp()

        f = Flight(departure_time=departure_time_stamp, arrival_time=arrival_time_stamp)
        self.assertEqual(f.duration.total_seconds(), 7200)

    def test_flight_number(self):
        flight_number = 1120
        f = Flight(flight_number=flight_number)
        self.assertEqual(f.flight_number, flight_number)

    def test_to_string(self):
        f = Flight(from_location="San Francisco", to_location="Orlando", from_location_code="SFO", to_location_code="MCO", departure_time=datetime(2020, 1, 1, 10, 10, 10).timestamp(), arrival_time=datetime(2020, 1, 1, 12, 10, 10).timestamp(), airline="UA", flight_number=1120)

        s = ""
        s += "Flight from San Francisco to Orlando\n"
        s += "    Departure Time: {}".format(datetime(2020, 1, 1, 10, 10, 10).strftime("%m/%d/%Y, %-I:%M %p")) + "\n"
        s += "    Arrival Time: {}".format(datetime(2020, 1, 1, 12, 10, 10).strftime("%m/%d/%Y, %-I:%M %p")) + "\n"
        s += "    Airline: UA\n"
        s += "    Duration: 2.0 hours\n"
        s += "    Flight Number: 1120\n"
        self.assertEqual(s, f.__str__())

    def test_build_flight(self):
        flight_data = {}
        flight_data["cityFrom"] = "San Francisco"
        flight_data["cityTo"] = "Orlando"
        flight_data["flyFrom"] = "SFO"
        flight_data["flyTo"] = "MCO"
        flight_data["dTimeUTC"] = datetime(2020, 1, 1, 10, 10, 10).timestamp()
        flight_data["aTimeUTC"] = datetime(2020, 1, 1, 12, 10, 10).timestamp()
        flight_data["airline"] = "UA"
        flight_data["flight_no"] = 1120

        f = Flight.build_flight(flight_data)

        self.assertEqual(f.from_location, flight_data["cityFrom"])
        self.assertEqual(f.from_location_code, flight_data["flyFrom"])
        self.assertEqual(f.to_location, flight_data["cityTo"])
        self.assertEqual(f.to_location_code, flight_data["flyTo"])
        self.assertEqual(f.departure_time.timestamp(), flight_data["dTimeUTC"])
        self.assertEqual(f.arrival_time.timestamp(), flight_data["aTimeUTC"])
        self.assertEqual(f.airline, flight_data["airline"])
        self.assertEqual(f.duration.total_seconds(), 7200)
        self.assertEqual(f.flight_number, flight_data["flight_no"])