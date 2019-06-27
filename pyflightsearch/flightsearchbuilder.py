from datetime import date, time
from util import build_flight_search_requests

class FlightSearchBuilder:
    # TODO(joshimbriani): Handle rollover of dates
    def __init__(self, from_location=None, to_location=None, departure_time=None, arrival_time=None, return_departure_time=None, return_arrival_time=None, departure_day=None, arrival_day=None, return_departure_day=None, return_arrival_day=None, price_threshold=None, start_from=date(date.year, date.month + 3, date.day)):
        if from_location:
            self.from_location = from_location
        if to_location:
            self.to_location = to_location
        if departure_time:
            self.departure_time = departure_time
        if arrival_time:
            self.arrival_time = arrival_time
        if return_departure_time:
            self.return_departure_time = return_departure_time
        if return_arrival_time:
            self.return_arrival_time = return_arrival_day
        if departure_day:
            self.departure_day = departure_day
        if arrival_day:
            self.arrival_day = arrival_day
        if return_departure_day:
            self.return_departure_day = return_departure_day
        if return_arrival_day:
            self.return_arrival_day = return_arrival_day
        if price_threshold:
            self.price_threshold = price_threshold
        self.start_from = start_from

    def from(self, location):
        self.from_location = location
        return self

    def to(self, location):
        self.to_location = location
        return self

    def departure_time(self, time_range):
        if type(time_range) != tuple:
            return ConfigurationError("Input to departure_time must be a tuple of string objects that represent times.")
        if not isinstance(time_range[0], time) or not isinstance(time_range[1], time):
            return ConfigurationError("Input to departure_time must be a tuple of string objects that represent times.")
        self.departure_time = time_range
        return self

    def arrival_time(self, time_range):
        if type(time_range) != tuple:
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        if not isinstance(time_range[0], time) or not isinstance(time_range[1], time):
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        self.return_time = time_range
        return self

    def return_departure_time(self, time_range):
        if type(time_range) != tuple:
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        if not isinstance(time_range[0], time) or not isinstance(time_range[1], time):
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        self.return_departure_time = time_range
        return self

    def return_arrival_time(self, time_range):
        if type(time_range) != tuple:
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        if not isinstance(time_range[0], time) or not isinstance(time_range[1], time):
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        self.return_arrival_time = time_range
        return self

    def weekend(self):
        self.departure_time = (time(hour=18, minute=0), time(hour=23, minute=59))
        self.return_time = (time(hour=0, minute=0), time(hour=23, minute=0))
        self.departure_day = "MO"
        self.return_arrival_day = "SU"
        return self

    def price_threshold(self, price):
        if type(price) != float or type(price) != int:
            return ConfigurationError("Input to price_threshold must be of type int or float")
        self.price_threshold = price
        return self

    def start_from(self, start_date):
        if type()

    def search(self):
        # validate request
        if not self.request_is_valid():
            return ConfigurationError("Invalid request")

        # build requests
        flight_requests = build_flight_search_requests(self)

        # make request
        trips = []
        for flight_request in flight_requests:
            trips.append(parse_flight_response())

        # parse request

        # return trip object
        pass