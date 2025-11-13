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
    {"latitude": 42.3144, "longitude": -71.0418, "velocity": 10.2, "battery": 99.8},
    {"latitude": 42.3146, "longitude": -71.0416, "velocity": 10.5, "battery": 99.6},
    {"latitude": 42.3148, "longitude": -71.0414, "velocity": 9.8,  "battery": 99.4},
    {"latitude": 42.3150, "longitude": -71.0412, "velocity": 11.0, "battery": 99.2},
    {"latitude": 42.3153, "longitude": -71.0409, "velocity": 10.7, "battery": 98.9},
    {"latitude": 42.3156, "longitude": -71.0406, "velocity": 10.0, "battery": 98.5},
    {"latitude": 42.3159, "longitude": -71.0403, "velocity": 9.9,  "battery": 98.1},
    {"latitude": 42.3162, "longitude": -71.0400, "velocity": 10.3, "battery": 97.8},
    {"latitude": 42.3165, "longitude": -71.0397, "velocity": 10.1, "battery": 97.5},
    {"latitude": 42.3168, "longitude": -71.0394, "velocity": 10.0, "battery": 97.2},
    {"latitude": 42.3170, "longitude": -71.0391, "velocity": 9.7,  "battery": 96.9},
    {"latitude": 42.3173, "longitude": -71.0388, "velocity": 9.8,  "battery": 96.7},
    {"latitude": 42.3176, "longitude": -71.0385, "velocity": 10.2, "battery": 96.4},
    {"latitude": 42.3179, "longitude": -71.0382, "velocity": 10.4, "battery": 96.0},
    {"latitude": 42.3182, "longitude": -71.0379, "velocity": 10.6, "battery": 95.6},
    {"latitude": 42.3185, "longitude": -71.0376, "velocity": 10.1, "battery": 95.3},
    {"latitude": 42.3188, "longitude": -71.0373, "velocity": 9.9,  "battery": 95.0},
    {"latitude": 42.3190, "longitude": -71.0370, "velocity": 9.6,  "battery": 94.8},
    {"latitude": 42.3193, "longitude": -71.0367, "velocity": 9.8,  "battery": 94.5},
    {"latitude": 42.3196, "longitude": -71.0364, "velocity": 10.0, "battery": 94.2},
    {"latitude": 42.3199, "longitude": -71.0361, "velocity": 10.3, "battery": 93.9},
    {"latitude": 42.3202, "longitude": -71.0358, "velocity": 10.5, "battery": 93.6},
    {"latitude": 42.3205, "longitude": -71.0355, "velocity": 10.2, "battery": 93.3}
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
