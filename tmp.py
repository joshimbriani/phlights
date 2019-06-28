from phlights.flightsearch import FlightSearch
from phlights.util import build_flight_search_queries
from datetime import date
def test():
    print(build_flight_search_queries(FlightSearch.weekend().from_place("SFO").to_place("MCO")._start_from(date.today())))

if __name__ == "__main__":
    test()