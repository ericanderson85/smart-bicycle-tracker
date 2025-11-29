import machine
import network
import time
import usocket as socket
import ujson as json

ENV_PATH = ".env"


def load_env(path=ENV_PATH):
    """Parse a simple KEY=VALUE env file into a dict."""
    env = {}
    try:
        with open(path) as env_file:
            for raw_line in env_file:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    except OSError:
        raise RuntimeError("Missing .env file; cannot start firmware")
    return env


env = load_env()

try:
    WIFI_SSID = env["WIFI_SSID"]
    WIFI_PASSWORD = env["WIFI_PASSWORD"]
    PORT = int(env["API_PORT"])
except KeyError as missing_key:
    raise RuntimeError("Required environment value missing: {}".format(missing_key))
except ValueError:
    raise RuntimeError("API_PORT must be an integer")

if not WIFI_SSID or not WIFI_PASSWORD:
    raise RuntimeError("WIFI_SSID and WIFI_PASSWORD must be non-empty")

# --- DATA ---
SAMPLE_DATA = [
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


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to network...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
            print(".", end="")
    print("\nNetwork config:", wlan.ifconfig())


def start_server():
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allows reusing the socket address immediately after restart
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind(("", PORT))
        s.listen(5)
    except OSError:
        print("Failed to bind to port. Resetting machine in 5 seconds.")
        time.sleep(5)
        machine.reset()

    print(f"Listening on port {PORT}...")

    data_index = 0

    while True:
        try:
            conn, _ = s.accept()
            request = conn.recv(1024)
            request_str = str(request)

            if "GET / " in request_str or "GET /HTTP" in request_str:
                # Get current data point
                current_data = SAMPLE_DATA[data_index % len(SAMPLE_DATA)]
                data_index += 1

                # Format JSON
                response_json = json.dumps(current_data)

                # Send Headers
                conn.send(b"HTTP/1.1 200 OK\r\n")
                conn.send(b"Content-Type: application/json\r\n")
                conn.send(b"Access-Control-Allow-Origin: *\r\n")
                conn.send(b"Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n")
                conn.send(b"Access-Control-Allow-Headers: Content-Type\r\n")
                conn.send(b"Connection: close\r\n\r\n")

                # Send Body
                conn.send(response_json.encode())

            elif "OPTIONS" in request_str:
                # Handle CORS pre-flight
                conn.send(b"HTTP/1.1 200 OK\r\n")
                conn.send(b"Access-Control-Allow-Origin: *\r\n")
                conn.send(b"Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n")
                conn.send(b"Access-Control-Allow-Headers: Content-Type\r\n")
                conn.send(b"Connection: close\r\n\r\n")

            else:
                # 404 for other routes
                conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")

            conn.close()

        except Exception as e:
            print("Error:", e)
            try:
                conn.close()
            except Exception:
                pass


# --- MAIN ---
try:
    connect_wifi()
    start_server()
except KeyboardInterrupt:
    print("Stopping server")
