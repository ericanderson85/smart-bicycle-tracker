from http.server import HTTPServer
from typing import TypedDict
from api_handler import APIHandler


class BikeData(TypedDict):
    latitude: float
    longitude: float
    velocity: float
    battery: float


# fmt: off
SAMPLE_DATA: list[BikeData] = [
    {"latitude": 42.3142, "longitude": -71.0420, "velocity": 10.0, "battery": 100.0},
    {"latitude": 42.31427, "longitude": -71.04193, "velocity": 10.2, "battery": 99.8},
    {"latitude": 42.31433, "longitude": -71.04187, "velocity": 10.5, "battery": 99.6},
    {"latitude": 42.3144, "longitude": -71.0418, "velocity": 9.8, "battery": 99.4},
    {"latitude": 42.31447, "longitude": -71.04173, "velocity": 11.0, "battery": 99.2},
    {"latitude": 42.31453, "longitude": -71.04163, "velocity": 10.7, "battery": 98.9},
    {"latitude": 42.3146, "longitude": -71.04153, "velocity": 10.0, "battery": 98.5},
    {"latitude": 42.31467, "longitude": -71.04143, "velocity": 9.9, "battery": 98.1},
    {"latitude": 42.31473, "longitude": -71.04133, "velocity": 10.3, "battery": 97.8},
    {"latitude": 42.3148, "longitude": -71.04123, "velocity": 10.1, "battery": 97.5},
    {"latitude": 42.31487, "longitude": -71.04113, "velocity": 10.0, "battery": 97.2},
    {"latitude": 42.31493, "longitude": -71.04103, "velocity": 9.7, "battery": 96.9},
    {"latitude": 42.315, "longitude": -71.04093, "velocity": 9.8, "battery": 96.7},
    {"latitude": 42.31507, "longitude": -71.04083, "velocity": 10.2, "battery": 96.4},
    {"latitude": 42.31513, "longitude": -71.04073, "velocity": 10.4, "battery": 96.0},
    {"latitude": 42.3152, "longitude": -71.04063, "velocity": 10.6, "battery": 95.6},
    {"latitude": 42.31527, "longitude": -71.04053, "velocity": 10.1, "battery": 95.3},
    {"latitude": 42.31533, "longitude": -71.04043, "velocity": 9.9, "battery": 95.0},
    {"latitude": 42.3154, "longitude": -71.04033, "velocity": 9.6, "battery": 94.8},
    {"latitude": 42.31547, "longitude": -71.04023, "velocity": 9.8, "battery": 94.5},
    {"latitude": 42.31553, "longitude": -71.04013, "velocity": 10.0, "battery": 94.2},
    {"latitude": 42.3156, "longitude": -71.04003, "velocity": 10.3, "battery": 93.9},
    {"latitude": 42.31567, "longitude": -71.03993, "velocity": 10.5, "battery": 93.6},
    {"latitude": 42.31573, "longitude": -71.03983, "velocity": 10.2, "battery": 93.3},
]
# fmt: on

API_PORT = 5001


class BikeServer:
    def __init__(self):
        self.data_index = 0
        self.sample_data = SAMPLE_DATA

        @APIHandler.get("/")
        def index(_: dict) -> BikeData:
            data = self.sample_data[self.data_index % len(self.sample_data)]
            self.data_index += 1
            return data

    def run(self, port: int):
        print(f"Serving on http://localhost:{port}")
        HTTPServer(("localhost", port), APIHandler).serve_forever()


if __name__ == "__main__":
    BikeServer().run(API_PORT)
