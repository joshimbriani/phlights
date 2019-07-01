from phlights.models.leg import Leg

class Trip:
    def __init__(self, price=None, from_location=None, from_location_code=None, to_location=None, to_location_code=None, legs=None):
        self._price = price
        self._from_location = from_location
        self._from_location_code = from_location_code
        self._to_location = to_location
        self._to_location_code = to_location_code
        self._legs = legs

    def add_legs(self, legs):
        self._legs = legs

    @property
    def price(self):
        return self._price

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
    def legs(self):
        return self._legs

    def __str__(self):
        trip = ""
        trip += "Trip from {} to {}".format(self.from_location, self.to_location) + "\n"
        trip += "    Price: ${}".format(self.price) + "\n"
        trip += "    Legs:" + "\n"
        for leg in self.legs:
            trip += "    " + str(leg) + "\n"

        return trip

    @staticmethod
    def build_trip(trip_response):
        t = Trip(price=trip_response["price"], from_location=trip_response["cityFrom"], from_location_code=trip_response["flyFrom"], to_location=trip_response["cityTo"], to_location_code=trip_response["flyTo"])
        t.add_legs(Leg.build_legs(trip_response["route"], trip_response["flyFrom"], trip_response["flyTo"], trip_response["cityFrom"], trip_response["cityTo"]))
        return t