import unittest
from datetime import datetime

from phlights.models.flight import Flight
from phlights.models.leg import Leg
from phlights.models.trip import Trip


class TripTest(unittest.TestCase):
    def test_empty_trip(self):
        t = Trip()

        self.assertEqual(t.from_location, "")
        self.assertEqual(t.from_location_code, "")
        self.assertEqual(t.to_location, "")
        self.assertEqual(t.to_location_code, "")
        self.assertEqual(t.price, -1)
        self.assertEqual(t.legs, [])
        self.assertEqual(t.book_url, "")

    def test_add_legs(self):
        t = Trip()
        self.assertEqual(t.legs, [])

        t.add_legs([[{"flight_number": 1}], [{"flight_number": 2}]])
        self.assertEqual(len(t.legs), 2)
        self.assertEqual(t.legs, [[{"flight_number": 1}], [{"flight_number": 2}]])

    def test_from_location(self):
        from_location = "San Francisco"
        t = Trip(from_location=from_location)
        self.assertEqual(t.from_location, from_location)

    def test_from_location_code(self):
        from_location_code = "SFO"
        t = Trip(from_location_code=from_location_code)
        self.assertEqual(t.from_location_code, from_location_code)

    def test_to_location(self):
        to_location = "SFO"
        t = Trip(to_location=to_location)
        self.assertEqual(t.to_location, to_location)

    def test_to_location_code(self):
        to_location_code = "SFO"
        t = Trip(to_location_code=to_location_code)
        self.assertEqual(t.to_location_code, to_location_code)

    def test_price(self):
        price = 100
        t = Trip(price=price)

        self.assertEqual(t.price, price)

    def test_book_url(self):
        book_url = "https://google.com"
        t = Trip(book_url=book_url)

        self.assertEqual(t.book_url, book_url)

    def test_to_string(self):
        f1 = Flight(from_location="San Francisco", to_location="Orlando", from_location_code="SFO", to_location_code="MCO", departure_time=datetime(2020, 1, 1, 10, 10, 10).timestamp(), arrival_time=datetime(2020, 1, 1, 12, 10, 10).timestamp(), airline="UA", flight_number=1120)
        f2 = Flight(from_location="Orlando", to_location="Columbus", from_location_code="MCO", to_location_code="CMH", departure_time=datetime(2020, 1, 1, 12, 10, 10).timestamp(), arrival_time=datetime(2020, 1, 1, 14, 10, 10).timestamp(), airline="UA", flight_number=1121)
        l1 = Leg(from_location="San Francisco", to_location="Orlando", from_location_code="SFO", to_location_code="CMH", departure_time=datetime(2020, 1, 1, 10, 10, 10).timestamp(), arrival_time=datetime(2020, 1, 1, 14, 10, 10).timestamp(), flights=[f1, f2])

        f3 = Flight(from_location="Columbus", to_location="Orlando", from_location_code="CMH", to_location_code="MCO", departure_time=datetime(2020, 1, 1, 16, 10, 10).timestamp(), arrival_time=datetime(2020, 1, 1, 18, 10, 10).timestamp(), airline="UA", flight_number=1122)
        f4 = Flight(from_location="Orlando", to_location="San Francisco", from_location_code="MCO", to_location_code="SFO", departure_time=datetime(2020, 1, 1, 18, 10, 10).timestamp(), arrival_time=datetime(2020, 1, 1, 20, 10, 10).timestamp(), airline="UA", flight_number=1123)
        l2 = Leg(from_location="Columbus", to_location="San Francisco", from_location_code="CMH", to_location_code="SFO", departure_time=datetime(2020, 1, 1, 16, 10, 10).timestamp(), arrival_time=datetime(2020, 1, 1, 20, 10, 10).timestamp(), flights=[f3, f4])

        t = Trip(price=100, from_location="San Francisco", from_location_code="SFO", to_location="Columbus", to_location_code="CMH", book_url="https://google.com")
        t.add_legs([l1, l2])

        s = ""
        s += "Trip from San Francisco to Columbus\n"
        s += "    Price: $100\n"
        s += "    Link: https://google.com\n"
        s += "    Legs:\n"
        s += "    " + l1.__str__() + "\n"
        s += "    " + l2.__str__() + "\n"
        self.assertEqual(s, t.__str__())
