from datetime import date, time, timedelta, datetime
from time import sleep

from phlights.util import build_flight_search_queries, make_api_request
from phlights.errors.configuration_error import ConfigurationError
from phlights.constants import Day, MAX_LOOKAHEAD_DAYS, API_BACKOFF_SECONDS
from phlights.models.trip import Trip

class FlightSearchBuilder:
    def __init__(self, from_location=None, to_location=None, departure_time=None, arrival_time=None, return_departure_time=None, return_arrival_time=None, departure_day=None, arrival_day=None, return_departure_day=None, return_arrival_day=None, price_threshold=None, start_from=(date.today() + timedelta(days=30)), allow_layovers=False, departure_date=None, return_departure_date=None):
        self._from_location = from_location
        self._to_location = to_location
        self._departure_time = departure_time
        self._arrival_time = arrival_time
        self._return_departure_time = return_departure_time
        self._return_arrival_time = return_arrival_time
        self._departure_day = departure_day
        self._arrival_day = arrival_day
        self._return_departure_day = return_departure_day
        self._return_arrival_day = return_arrival_day
        self._price_threshold = price_threshold
        self._start_from = start_from
        self._allow_layovers = allow_layovers
        self._departure_date = departure_date
        self._return_departure_date = return_departure_date

    def from_place(self, location):
        self._from_location = location
        return self

    def to_place(self, location):
        self._to_location = location
        return self

    def departure_date(self, departure_date):
        if not isinstance(departure_date, date):
            return ConfigurationError("Input to departure_date must be of type datetime")
        self._departure_date = departure_date
        return self

    def departure_time(self, time_range):
        if type(time_range) != tuple:
            return ConfigurationError("Input to departure_time must be a tuple of string objects that represent times.")
        if not isinstance(time_range[0], time) or not isinstance(time_range[1], time):
            return ConfigurationError("Input to departure_time must be a tuple of string objects that represent times.")
        self._departure_time = time_range
        return self

    def arrival_time(self, time_range):
        if type(time_range) != tuple:
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        if not isinstance(time_range[0], time) or not isinstance(time_range[1], time):
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        self._return_time = time_range
        return self

    def return_departure_date(self, return_departure_date):
        if not isinstance(return_departure_date, date):
            return ConfigurationError("Input to departure_date must be of type datetime")
        self._return_departure_date = return_departure_date
        return self

    def return_departure_time(self, time_range):
        if type(time_range) != tuple:
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        if not isinstance(time_range[0], time) or not isinstance(time_range[1], time):
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        self._return_departure_time = time_range
        return self

    def return_arrival_time(self, time_range):
        if type(time_range) != tuple:
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        if not isinstance(time_range[0], time) or not isinstance(time_range[1], time):
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        self._return_arrival_time = time_range
        return self

    def weekend(self):
        self._departure_time = (time(hour=18, minute=0), time(hour=23, minute=59))
        #self._arrival_time = (time(hour=0, minute=0), time(hour=6, minute=0))
        self._return_arrival_time = (time(hour=0, minute=0), time(hour=23, minute=00))
        self._departure_day = Day.FRIDAY
        self._return_arrival_day = Day.SUNDAY
        return self

    def price_threshold(self, price):
        if type(price) != float and type(price) != int:
            return ConfigurationError("Input to price_threshold must be of type int or float")
        self._price_threshold = price
        return self

    def start_from(self, start_date):
        if not isinstance(start_date, date):
            return ConfigurationError("Input to start_from must be of type date")
        self._start_from = start_date
        return self

    def allow_layovers(self, allow_layovers):
        if type(allow_layovers) != bool:
            return ConfigurationError("Input to allow_layovers must be of type boolean")
        self._allow_layovers = allow_layovers
        return self

    def search(self):
        # validate request
        if not self.request_is_valid():
            return ConfigurationError("Invalid request")

        # build requests
        flight_queries = build_flight_search_queries(self)

        # make request
        trips = []
        for flight_query in flight_queries:
            trip = parse_flight_response(make_api_request(flight_query))
            if trip:
                trips.extend(trip)
            sleep(API_BACKOFF_SECONDS)

        # return trip object
        trips.sort(key=lambda trip: trip.price)
        return trips

    def request_is_valid(self):
        if not self._to_location or not self._from_location:
            return False

        return True

    def get_departure_time_string(self):
        if not self._departure_time:
            return None
        return (self._departure_time[0].strftime("%H:%M"), self._departure_time[1].strftime("%H:%M"))

    def get_arrival_time_string(self):
        if not self._arrival_time:
            return None
        return (self._arrival_time[0].strftime("%H:%M"), self._arrival_time[1].strftime("%H:%M"))

    def get_return_departure_time_string(self):
        if not self._return_departure_time:
            return None
        return (self._return_departure_time[0].strftime("%H:%M"), self._return_departure_time[1].strftime("%H:%M"))

    def get_return_arrival_time_string(self):
        if not self._return_arrival_time:
            return None
        return (self._return_arrival_time[0].strftime("%H:%M"), self._return_arrival_time[1].strftime("%H:%M"))

    def get_date_range(self):
        if not self._start_from:
            return None
        return (self._start_from, (self._start_from + timedelta(MAX_LOOKAHEAD_DAYS)))

    def get_date_range_string(self):
        if not self._start_from:
            return None
        return (self._start_from.strftime("%d/%m/%Y"), (self._start_from + timedelta(MAX_LOOKAHEAD_DAYS)).strftime("%d/%m/%Y"))

def parse_flight_response(flight_response):
    if not flight_response:
        return None

    trips = []
    for trip in flight_response:
        trips.append(Trip.build_trip(trip))

    return trips