from datetime import datetime

import pytz
from tzlocal import get_localzone

# TODO(joshimbriani): Use tz?
class Flight:
    def __init__(self, from_location="", from_location_code="", to_location="", to_location_code="", departure_time=None, arrival_time=None, airline="", flight_number=None):
        self._from_location = from_location
        self._from_location_code = from_location_code
        self._to_location = to_location
        self._to_location_code = to_location_code
        self._departure_time = departure_time
        self._arrival_time = arrival_time
        self._airline = airline
        self._flight_number = flight_number

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
    def airline(self):
        return self._airline

    @property
    def duration(self):
        if not self._arrival_time or not self._departure_time:
            return 0

        return datetime.utcfromtimestamp(self._arrival_time) - datetime.utcfromtimestamp(self._departure_time)

    @property
    def flight_number(self):
        if not self._flight_number:
            return -1
        return self._flight_number

    @staticmethod
    def build_flight(flight_data):
        f = Flight()

        f._from_location = flight_data["cityFrom"]
        f._to_location = flight_data["cityTo"]
        f._from_location_code = flight_data["flyFrom"]
        f._to_location_code = flight_data["flyTo"]
        f._departure_time = flight_data["dTimeUTC"]
        f._arrival_time = flight_data["aTimeUTC"]
        f._airline = flight_data["airline"]
        f._flight_number = flight_data["flight_no"]

        return f

    def __str__(self):
        s = ""
        s += "Flight from {} to {}".format(self.from_location, self.to_location) + "\n"
        s += "    Departure Time: {}".format(self.departure_time.strftime("%m/%d/%Y, %-I:%M %p")) + "\n"
        s += "    Arrival Time: {}".format(self.arrival_time.strftime("%m/%d/%Y, %-I:%M %p")) + "\n"
        s += "    Airline: {}".format(self.airline) + "\n"
        s += "    Duration: {} hours".format(self.duration.total_seconds()/60/60) + "\n"
        s += "    Flight Number: {}".format(self.flight_number) + "\n"

        return s