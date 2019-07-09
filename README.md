# Phlights

Phlights is a Python API that wraps the [Kiwi Flight API](https://docs.kiwi.com/), providing some easy to consume objects and search methods.

## Example

This code searches for all weekend flights with no or one layovers from San Francisco to Orlando starting from 8/1/2019

```for trip in FlightSearch.weekend().from_place("SFO").to_place("MCO").start_from(date(year=2019, month=8, day=1)).allow_layovers(True).search():
        print(trip)
```

## Documentation

### Flight

#### Properties

| Property        | Accessor           | Description  | Type    |
| ------------- |:-------------:| -----:| ------:|
| from_location      | _from_location | The full name of the city the plane departs from  | string |
| from_location_code      | _from_location_code      |   The airport code for the city the plane departs from | string |
| to_location      | _to_location | The full name of the city the plane arrives at  | string |
| to_location_code      | _to_location_code      |   The airport code for the city the plane arrives at | string |
| arrival_time      | _arrival_time      |   The departure time (in local time) of the flight | time |
| departure_time      | _departure_time      |   The arrival time (in local time) of the flight | time |
| airline      | _airline      |   The airline operating the flight | string |
| flight_number      | _flight_number      |   The flight number of the flight | int |

#### Static Methods

| Method        | Params           | Return  |
| ------------- |:-------------:| -----:|
| build_flight      | flight_data: json object | A Flight object |

### Leg

#### Properties

| Property        | Accessor           | Description  | Type    |
| ------------- |:-------------:| -----:| ------:|
| from_location      | _from_location | The full name of the city the plane departs from  | string |
| from_location_code      | _from_location_code      |   The airport code for the city the plane departs from | string |
| to_location      | _to_location | The full name of the city the plane arrives at  | string |
| to_location_code      | _to_location_code      |   The airport code for the city the plane arrives at | string |
| arrival_time      | _arrival_time      |   The departure time (in local time) of the leg | time |
| departure_time      | _departure_time      |   The arrival time (in local time) of the leg | time |
| flights      | _flights      |   An array of the Flight objects that make up the leg | array of Flight objects |
| layovers      | Cannot Set      |   The number of layovers on the leg | int |
| duration      | Cannot Set      |   The duration of the leg in seconds | int |

#### Static Methods

| Method        | Params           | Return  |
| ------------- |:-------------:| -----:|
| build_legs      | flight_data: json_object, start: airport code string, end: airport code string, start_city: city name string, end_city: city name string | A Leg object |

### Trip

#### Properties

| Property        | Accessor           | Description  | Type    |
| ------------- |:-------------:| -----:| ------:|
| from_location      | _from_location | The full name of the city the plane departs from  | string |
| from_location_code      | _from_location_code      |   The airport code for the city the plane departs from | string |
| to_location      | _to_location | The full name of the city the plane arrives at  | string |
| to_location_code      | _to_location_code      |   The airport code for the city the plane arrives at | string |
| price      | _price      |   The price of the trip | int |
| legs      | _legs      |   The legs that make up the trip | array of Leg objects |
| book_url      | _book_url      |   The URL to book the trip | string |

#### Static Methods

| Method        | Params           | Return  |
| ------------- |:-------------:| -----:|
| build_trip      | trip_response: json_object | A Trip object |

### Flight Search Builder

#### Methods

| Method        | Params           | Return  | Description |
| ------------- |:-------------:| -----:| ----------------:|
| from_place      | location: airport code string | A FlightSearchBuilder object | Add a from location to the FSB object; necessary for searching |
| to_place      | location: string | A FlightSearchBuilder object | Add a to location to the FSB object; necessary for searching |
| departure_date      | departure_date: datetime | A FlightSearchBuilder object | Add a start departure date|
| departure_time     | time_range: tuple of 2 time objects | A FlightSearchBuilder object | Add a time range when you want your flight to leave |
| arrival_time      | time_range: tuple of 2 time objects | A FlightSearchBuilder object | Add a time range when you want your flight to arrive at the destination |
| return_departure_date      | return_departure_date: datetime | A FlightSearchBuilder object | Add a return departure date to your flight|
| return_departure_time     | time_range: tuple of 2 time objects | A FlightSearchBuilder object | Add a time range when you want your return flight to depart|
| return_arrival_time     | time_range: tuple of 2 time objects | A FlightSearchBuilder object | Add a time range when you want your return flight to arrive|
| weekend     | | A FlightSearchBuilder object | A convenience method that sets the departure day to Friday after 6pm, return departure day to Sunday all day and the nights in destination at 1-2|
| price_threshold     | price: int | A FlightSearchBuilder object | The maximum price you're willing to pay for the flight|
| start_from     | start_date: date | A FlightSearchBuilder object | The day you want to start searhing for flights from|
| allow_layovers     | allow_layovers: bool | A FlightSearchBuilder object | Whether to allow layovers or not|
| search     | | List of Trip objects | Start a search with the given parameters. Returns a lit of trip objects |

### Flight Search

Mimics Flight Search Builder API methods. Returns a FlightSearchBuilder object