from datetime import datetime

# TODO(joshimbriani): 
class Flight:
    def __init__(self, from_location=None, from_location_code=None, to_location=None, to_location_code=None, departure_time=None, arrival_time=None, airline=None, duration=None, flight_number=None):
        self._from_location = from_location
        self._from_location_code = from_location_code
        self._to_location = to_location
        self._to_location_code = to_location_code
        self._departure_time = departure_time
        self._arrival_time = arrival_time
        self._airline = airline
        self._duration = duration
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
        return datetime.fromtimestamp(self._departure_time)

    @property
    def arrival_time(self):
        return datetime.fromtimestamp(self._arrival_time)

    @property
    def airline(self):
        return self._airline

    @property
    def duration(self):
        return self._duration

    @property
    def flight_number(self):
        return self._flight_number

    @staticmethod
    def build_flight(flight_data):
        f = Flight()

        f._from_location = flight_data["cityFrom"]
        f._to_location = flight_data["cityTo"]
        f._from_location_code = flight_data["flyFrom"]
        f._to_location_code = flight_data["flyTo"]
        f._departure_time = flight_data["dTime"]
        f._arrival_time = flight_data["aTime"]
        f._airline = flight_data["airline"]
        f._duration = flight_data["aTime"] - flight_data["dTime"]
        f._flight_number = flight_data["flight_no"]

        return f

    def __str__(self):
        s = ""
        s += "Flight from {} to {}".format(self.from_location, self.to_location) + " \n"
        s += "    Departure Time: {}".format(self.departure_time.strftime("%m/%d/%Y, %H:%M:%S")) + " \n"
        s += "    Arrival Time: {}".format(self.arrival_time.strftime("%m/%d/%Y, %H:%M:%S")) + "\n"
        s += "    Airline: {}".format(self.airline) + "\n"
        s += "    Duration: {}".format(self.duration) + "\n"
        s += "    Flight Number: {}".format(self.flight_number) + "\n"

        return s