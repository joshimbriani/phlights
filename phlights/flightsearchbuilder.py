from datetime import date, time, timedelta

from phlights.util import build_flight_search_queries
from phlights.errors.configuration_error import ConfigurationError
from phlights.constants import Day

class FlightSearchBuilder:
    def __init__(self, from_location=None, to_location=None, departure_time=None, arrival_time=None, return_departure_time=None, return_arrival_time=None, departure_day=None, arrival_day=None, return_departure_day=None, return_arrival_day=None, price_threshold=None, start_from=(date.today() + timedelta(days=30))):
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

    def from_place(self, location):
        self._from_location = location
        return self

    def to_place(self, location):
        self._to_location = location
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
        self._return_time = (time(hour=0, minute=0), time(hour=23, minute=00))
        self._departure_day = Day.FRIDAY
        self._return_arrival_day = Day.SUNDAY
        return self

    def price_threshold(self, price):
        if type(price) != float or type(price) != int:
            return ConfigurationError("Input to price_threshold must be of type int or float")
        self._price_threshold = price
        return self

    def start_from(self, start_date):
        if not isinstance(start_date, date):
            return ConfigurationError("Input to start_from must be of type date")
        self._start_from = start_date
        return self

    def search(self):
        return build_flight_search_queries(self)

        # validate request
        if not self.request_is_valid():
            return ConfigurationError("Invalid request")

        # build requests
        flight_requests = build_flight_search_queries(self)

        # make request
        trips = []
        for flight_request in flight_requests:
            trips.append(parse_flight_response())

        # parse request

        # return trip object
        pass

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
        return (self._start_from, (self._start_from + timedelta(90)))

    def get_date_range_string(self):
        if not self._start_from:
            return None
        return (self._start_from.strftime("%d/%m/%Y"), (self._start_from + timedelta(90)).strftime("%d/%m/%Y"))