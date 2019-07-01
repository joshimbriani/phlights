from phlights.flightsearch import FlightSearch
from phlights.util import build_flight_search_queries
from datetime import date
def test():
    for trip in FlightSearch.weekend().from_place("SFO").to_place("MCO").start_from(date(year=2019, month=8, day=1)).search():
        print(trip)

if __name__ == "__main__":
    test()