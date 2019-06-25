from flightsearchbuilder import FlightSearchBuilder
from errors.configuration_error import ConfigurationError
from datetime import time

class FlightSearch:
    @staticmethod
    def from(location):
        return FlightSearchBuilder(from_location=location)

    @staticmethod
    def to(location):
        return FlightSearchBuilder(to_location=location)

    @staticmethod
    def departure_time(time_range):
        if type(time_range) != tuple:
            return ConfigurationError("Input to departure_time must be a tuple of string objects that represent times.")
        if not isinstance(time_range[0], time) or not isinstance(time_range[1], time):
            return ConfigurationError("Input to departure_time must be a tuple of string objects that represent times.")
        return FlightSearchBuilder(departure_time=time_range)

    @staticmethod
    def arrival_time(time_range):
        if type(time_range) != tuple:
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        if not isinstance(time_range[0], time) or not isinstance(time_range[1], time):
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        return FlightSearchBuilder(arrival_time=time_range)

    @staticmethod
    def return_departure_time(time_range):
        if type(time_range) != tuple:
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        if not isinstance(time_range[0], time) or not isinstance(time_range[1], time):
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        return FlightSearchBuilder(return_departure_time=time_range)

    @staticmethod
    def return_arrival_time(time_range):
        if type(time_range) != tuple:
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        if not isinstance(time_range[0], time) or not isinstance(time_range[1], time):
            return ConfigurationError("Input to arrival_time must be a tuple of string objects that represent times.")
        return FlightSearchBuilder(return_arrival_time=time_range)

    @staticmethod
    def weekend():
        departure_time_range = (time(hour=18, minute=0), time(hour=23, minute=59))
        return_time_range = (time(hour=0, minute=0), time(hour=23, minute=0))
        departure_day = "MO"
        return_arrival_day = "SU"
        return FlightSearchBuilder(departure_time=departure_time_range, return_arrival_time=return_time_range, departure_day=departure_day, return_arrival_day=return_arrival_day)