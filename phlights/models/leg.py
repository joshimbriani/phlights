import math
from datetime import datetime

import pytz
from tzlocal import get_localzone

from phlights.errors.configuration_error import ConfigurationError
from phlights.util import find_route
from phlights.models.flight import Flight

class Leg:
    def __init__(self, departure_time=None, arrival_time=None, flights=None, from_location="", from_location_code="", to_location="", to_location_code=""):
        self._departure_time = departure_time
        self._arrival_time = arrival_time
        self._flights = flights
        self._from_location = from_location
        self._from_location_code = from_location_code
        self._to_location = to_location
        self._to_location_code = to_location_code

    @property
    def departure_time(self):
        if not self._departure_time:
            return datetime.utcfromtimestamp(0)

        local_tz = get_localzone()
        return datetime.utcfromtimestamp(self._departure_time).replace(tzinfo=pytz.utc).astimezone(local_tz)

    @property
    def arrival_time(self):
        if not self._arrival_time:
            return datetime.utcfromtimestamp(0)
        
        local_tz = get_localzone()
        return datetime.utcfromtimestamp(self._arrival_time).replace(tzinfo=pytz.utc).astimezone(local_tz)

    @property
    def flights(self):
        if not self._flights:
            return []

        return self._flights

    @property
    def from_location(self):
        return self._from_location

    @property
    def from_location_code(self):
        return self._from_location_code

    @property
    def to_location(self):
        return self._to_location

    @property
    def to_location_code(self):
        return self._to_location_code

    @property
    def layovers(self):
        if not self._flights:
            return -1
        
        return len(self._flights) - 1

    @property
    def duration(self):
        if not self._arrival_time or not self._departure_time:
            return 0

        return datetime.utcfromtimestamp(self._arrival_time) - datetime.utcfromtimestamp(self._departure_time)

    @staticmethod
    def build_legs(flight_data, start, end, start_city, end_city):
        # First find the route from start to end
        departure_route = find_route(flight_data, start, end)
        if not departure_route:
            return ConfigurationError("Couldn't determine route.")
        
        departure_leg = Leg()
        departure_flight_params = generate_leg_params(departure_route)

        departure_leg._flights = departure_flight_params[0]
        departure_leg._departure_time = departure_flight_params[1]
        departure_leg._arrival_time = departure_flight_params[2]

        departure_leg._from_location_code = start
        departure_leg._from_location = start_city
        departure_leg._to_location_code = end
        departure_leg._to_location = end_city

        # Then find the route from end to start
        arrival_route = find_route(flight_data, end, start)
        if not arrival_route:
            return ConfigurationError("Couldn't determine route.")
        
        return_leg = Leg()
        return_flight_params = generate_leg_params(arrival_route)

        return_leg._flights = return_flight_params[0]
        return_leg._departure_time = return_flight_params[1]
        return_leg._arrival_time = return_flight_params[2]

        return_leg._from_location_code = end
        return_leg._from_location = end_city
        return_leg._to_location_code = start
        return_leg._to_location = start_city

        return [departure_leg, return_leg]

    def __str__(self):
        s = ""
        s += "Leg from {} to {}".format(self.from_location, self.to_location) + "\n"
        s += "    Duration: {} hours".format(self.duration.total_seconds()/60/60) + "\n"
        s += "    Layovers: {}".format(self.layovers) + "\n"
        for flight in self.flights:
            s += "    " + str(flight) + "\n"

        return s


def generate_leg_params(all_flights):
    flights = []
    departure_time = math.inf
    arrival_time = -math.inf

    for flight in all_flights:
        flights.append(Flight.build_flight(flight))
        departure_time = min(departure_time, flight["dTimeUTC"])
        arrival_time = max(arrival_time, flight["aTimeUTC"])

    return [flights, departure_time, arrival_time]