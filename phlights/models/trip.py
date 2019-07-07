from phlights.models.leg import Leg

# TODO(joshimbriani): Handle non round trip flights
class Trip:
    def __init__(self, price=None, from_location="", from_location_code="", to_location="", to_location_code="", legs=None, book_url=""):
        self._price = price
        self._from_location = from_location
        self._from_location_code = from_location_code
        self._to_location = to_location
        self._to_location_code = to_location_code
        self._legs = legs
        self._book_url = book_url

    def add_legs(self, legs):
        self._legs = legs

    @property
    def price(self):
        if not self._price:
            return -1
        
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
        if not self._legs:
            return []
            
        return self._legs

    @property
    def book_url(self):
        return self._book_url

    def __str__(self):
        trip = ""
        trip += "Trip from {} to {}".format(self.from_location, self.to_location) + "\n"
        trip += "    Price: ${}".format(self.price) + "\n"
        trip += "    Link: {}".format(self.book_url) + "\n"
        trip += "    Legs:" + "\n"
        for leg in self.legs:
            trip += "    " + str(leg) + "\n"

        return trip

    @staticmethod
    def build_trip(trip_response):
        t = Trip(price=trip_response["price"], from_location=trip_response["cityFrom"], from_location_code=trip_response["flyFrom"], to_location=trip_response["cityTo"], to_location_code=trip_response["flyTo"], book_url=trip_response["deep_link"])
        t.add_legs(Leg.build_legs(trip_response["route"], trip_response["flyFrom"], trip_response["flyTo"], trip_response["cityFrom"], trip_response["cityTo"]))
        return t