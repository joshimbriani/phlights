from datetime import time, date

from phlights.errors.configuration_error import ConfigurationError
from phlights.flightsearchbuilder import FlightSearchBuilder
from phlights.constants import Day

class FlightSearch:
    @staticmethod
    def from_place(location):
        return FlightSearchBuilder(from_location=location)

    @staticmethod
    def to_place(location):
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
        #arrival_time_range = (time(hour=0, minute=0), time(hour=6, minute=0))
        departure_day = Day.FRIDAY
        return_arrival_day = Day.SUNDAY
        return FlightSearchBuilder(departure_time=departure_time_range, return_arrival_time=return_time_range, departure_day=departure_day, return_arrival_day=return_arrival_day)

    @staticmethod
    def price_threshold(self, price):
        if type(price) != float or type(price) != int:
            return ConfigurationError("Input to price_threshold must be of type int or float")
        return FlightSearchBuilder(price_threshold=price)

    @staticmethod
    def start_from(self, start_date):
        if not isinstance(start_date, date):
            return ConfigurationError("Input to start_from must be of type date")
        return FlightSearchBuilder(start_from=start_date)

    @staticmethod
    def allow_layovers(self, allow_layovers):
        if type(allow_layovers) != bool:
            return ConfigurationError("Input to allow_layovers must be of type bool")
        return FlightSearchBuilder(allow_layovers=allow_layovers)
        
