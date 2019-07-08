from datetime import date, time, datetime
import unittest

from phlights.flightsearchbuilder import FlightSearchBuilder
from phlights.flightsearch import FlightSearch
from phlights.constants import Day

# TODO(joshimbriani): Need to add __eq__ to models
class FlightSearchTest(unittest.TestCase):
    def test_from_place(self):
        f1 = FlightSearchBuilder().from_place("SFO")
        f2 = FlightSearch.from_place("SFO")
        f3 = FlightSearchBuilder(from_location="SFO")
        
        self.assertEqual(f1._from_location, f2._from_location)
        self.assertEqual(f2._from_location, f3._from_location)

    def test_to_place(self):
        f1 = FlightSearchBuilder().to_place("SFO")
        f2 = FlightSearch.to_place("SFO")
        f3 = FlightSearchBuilder(to_location="SFO")
        
        self.assertEqual(f1._to_location, f2._to_location)
        self.assertEqual(f2._to_location, f3._to_location)

    def test_departure_date(self):
        f1 = FlightSearchBuilder().departure_date(datetime(2020,1,1))
        f2 = FlightSearch.departure_date(datetime(2020,1,1))
        f3 = FlightSearchBuilder(departure_date=datetime(2020,1,1))
        
        self.assertEqual(f1._departure_date, f2._departure_date)
        self.assertEqual(f2._departure_date, f3._departure_date)

    def test_departure_time(self):
        f1 = FlightSearchBuilder().departure_time((time(0,0,1), time(0,0,2)))
        f2 = FlightSearch.departure_time((time(0,0,1), time(0,0,2)))
        f3 = FlightSearchBuilder(departure_time=(time(0,0,1), time(0,0,2)))
        
        self.assertEqual(f1._departure_date, f2._departure_date)
        self.assertEqual(f2._departure_date, f3._departure_date)

    def test_arrival_time(self):
        f1 = FlightSearchBuilder().arrival_time((time(0,0,1), time(0,0,2)))
        f2 = FlightSearch.arrival_time((time(0,0,1), time(0,0,2)))
        f3 = FlightSearchBuilder(arrival_time=(time(0,0,1), time(0,0,2)))
        
        self.assertEqual(f1._departure_date, f2._departure_date)
        self.assertEqual(f2._departure_date, f3._departure_date)

    def test_return_departure_date(self):
        f1 = FlightSearchBuilder().return_departure_date(datetime(2020,1,1))
        f2 = FlightSearch.return_departure_date(datetime(2020,1,1))
        f3 = FlightSearchBuilder(return_departure_date=datetime(2020,1,1))
        
        self.assertEqual(f1._departure_date, f2._departure_date)
        self.assertEqual(f2._departure_date, f3._departure_date)

    def test_return_departure_time(self):
        f1 = FlightSearchBuilder().return_departure_time((time(0,0,1), time(0,0,2)))
        f2 = FlightSearch.return_departure_time((time(0,0,1), time(0,0,2)))
        f3 = FlightSearchBuilder(return_departure_time=(time(0,0,1), time(0,0,2)))
        
        self.assertEqual(f1._departure_date, f2._departure_date)
        self.assertEqual(f2._departure_date, f3._departure_date)

    def test_return_arrival_time(self):
        f1 = FlightSearchBuilder().return_arrival_time((time(0,0,1), time(0,0,2)))
        f2 = FlightSearch.return_arrival_time((time(0,0,1), time(0,0,2)))
        f3 = FlightSearchBuilder(return_arrival_time=(time(0,0,1), time(0,0,2)))
        
        self.assertEqual(f1._departure_date, f2._departure_date)
        self.assertEqual(f2._departure_date, f3._departure_date)

    def test_weekend(self):
        f1 = FlightSearchBuilder().weekend()
        f2 = FlightSearch.weekend()
        f3 = FlightSearchBuilder(departure_time=(time(hour=18, minute=0), time(hour=23, minute=59)), return_arrival_time=(time(hour=0, minute=0), time(hour=23, minute=0)), departure_day=Day.FRIDAY, return_arrival_day=Day.SUNDAY)
        
        self.assertEqual(f1._departure_time, f2._departure_time)
        self.assertEqual(f2._departure_time, f3._departure_time)

        self.assertEqual(f1._return_arrival_time, f2._return_arrival_time)
        self.assertEqual(f2._return_arrival_time, f3._return_arrival_time)

        self.assertEqual(f1._departure_day, f2._departure_day)
        self.assertEqual(f2._departure_day, f3._departure_day)

        self.assertEqual(f1._return_arrival_day, f2._return_arrival_day)
        self.assertEqual(f2._return_arrival_day, f3._return_arrival_day)


    def test_price_threshold(self):
        f1 = FlightSearchBuilder().price_threshold(100)
        f2 = FlightSearch.price_threshold(100)
        f3 = FlightSearchBuilder(price_threshold=100)
        
        self.assertEqual(f1._price_threshold, f2._price_threshold)
        self.assertEqual(f2._price_threshold, f3._price_threshold)

    def test_start_from(self):
        f1 = FlightSearchBuilder().start_from(datetime(2020,1,1))
        f2 = FlightSearch.start_from(datetime(2020,1,1))
        f3 = FlightSearchBuilder(start_from=datetime(2020,1,1))
        
        self.assertEqual(f1._start_from, f2._start_from)
        self.assertEqual(f2._start_from, f3._start_from)

    def test_allow_layovers(self):
        f1 = FlightSearchBuilder().allow_layovers(True)
        f2 = FlightSearch.allow_layovers(True)
        f3 = FlightSearchBuilder(allow_layovers=True)
        
        self.assertEqual(f1._allow_layovers, f2._allow_layovers)
        self.assertEqual(f2._allow_layovers, f3._allow_layovers)

    def test_request_is_valid_valid_request(self):
        f1 = FlightSearchBuilder().from_place("SFO").to_place("MCO")

        self.assertTrue(f1.request_is_valid())

    def test_request_is_valid_invalid_request(self):
        f1 = FlightSearchBuilder().from_place("SFO")

        self.assertFalse(f1.request_is_valid())

    def test_get_date_range(self):
        f1 = FlightSearchBuilder().start_from(datetime(2020,1,1))

        date_range = f1.get_date_range()
        self.assertEqual(date_range[0], datetime(2020,1,1))
        self.assertEqual(date_range[1], datetime(2020,3,1))

    def test_chain_elements(self):
        f1 = FlightSearchBuilder().from_place("SFO").to_place("MCO").allow_layovers(True).price_threshold(100)
        f2 = FlightSearchBuilder(from_location="SFO", to_location="MCO", allow_layovers=True, price_threshold=100)

        self.assertEqual(f1._from_location, f2._from_location)
        self.assertEqual(f1._to_location, f2._to_location)
        self.assertEqual(f1._allow_layovers, f2._allow_layovers)
        self.assertEqual(f1._price_threshold, f2._price_threshold)

    def test_overwrite_fields(self):
        f1 = FlightSearchBuilder().from_place("SFO").from_place("MCO")

        self.assertEqual(f1._from_location, "MCO")
    