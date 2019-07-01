import unittest
from datetime import datetime

from phlights.models.flight import Flight

class FlightTest(unittest.TestCase):
    def test_empty_flight(self):
        pass

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
        departure_time = datetime(2020, 1, 1, 10, 10, 10)
        departure_time_stamp = departure_time.timestamp()
        f = Flight(departure_time=departure_time_stamp)
        self.assertEqual(f.departure_time, departure_time)

    def test_arrival_time(self):
        arrival_time = datetime(2020, 1, 1, 10, 10, 10)
        arrival_time_stamp = arrival_time.timestamp()
        f = Flight(arrival_time=arrival_time_stamp)
        self.assertEqual(f.arrival_time, arrival_time)

    def test_airline(self):
        airline = "UA"
        f = Flight(airline=airline)
        self.assertEqual(f.airline, airline)

    def test_flight_number(self):
        flight_number = 1120
        f = Flight(flight_number=flight_number)
        self.assertEqual(f.flight_number, flight_number)

    def test_build_flight(self):
        self.assertTrue(True)