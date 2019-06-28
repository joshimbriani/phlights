from datetime import datetime

class Flight:
    def __init__(self, departureTime, arrivalTime, airline, duration):
        if isinstance(departureTime, datetime):
            self.departureTime = departureTime
        elif type(departureTime) is int:
            self.departureTime = datetime.utcfromtimestamp(departureTime)
        else:
            # throw error
        
        if isinstance(arrivalTime, datetime):
            self.arrivalTime = arrivalTime
        elif type(arrivalTime) is int:
            self.arrivalTime = datetime.utcfromtimestamp(arrivalTime)
        else:
            # throw error

        self.airline = airline
        self.duration = duration