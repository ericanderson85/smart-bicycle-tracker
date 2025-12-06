import machine
import network
import uasyncio
from uasyncio import StreamReader, StreamWriter
import ujson
import gc
from gps_controller import GPSController
import time

ENV_PATH = ".env"


def load_env(path=ENV_PATH):
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
        raise RuntimeError("Missing .env file")
    return env


env = load_env()
WIFI_SSID = env.get("WIFI_SSID")
WIFI_PASSWORD = env.get("WIFI_PASSWORD")
PORT = env.get("API_PORT")
if not (WIFI_SSID and WIFI_PASSWORD and PORT):
    raise RuntimeError("Incorrect .env file")
PORT = int(PORT)

gps_controller = GPSController()


def connect_wifi():
    """
    Connect to WiFi. Blocks indefinitely until connected.
    If it fails for too long, it resets the machine to clear hardware states.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(dhcp_hostname="gps-tracker")

    if not wlan.isconnected():
        print(f"Connecting to {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        attempt_count = 0
        while not wlan.isconnected():
            attempt_count += 1
            time.sleep(1)
            print(".", end="")

            # If no connection after 30 seconds, hard reset
            if attempt_count > 30:
                print("\nWifi failed. Resetting machine...")
                machine.reset()

    print("\nNetwork config:", wlan.ifconfig())


async def handle_client(reader: StreamReader, writer: StreamWriter):
    try:
        request_line = await reader.readline()

        # Robustly skip headers (handle empty reads)
        while True:
            header = await reader.readline()
            if not header or header == b"\r\n":
                break

        if not request_line:
            # Connection opened but no data sent (common scanner behavior)
            writer.close()
            await writer.wait_closed()
            return

        request_str = request_line.decode("utf-8")
        print(f"Request: {request_str.strip()}")  # Debug print

        # Standard CORS headers required for ALL responses
        cors_headers = (
            b"Access-Control-Allow-Origin: *\r\n"
            b"Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
            b"Access-Control-Allow-Headers: *\r\n"
        )

        if "OPTIONS" in request_str:
            # Handle Preflight
            writer.write(b"HTTP/1.1 204 No Content\r\n")
            writer.write(cors_headers)
            writer.write(b"Connection: close\r\n\r\n")

        elif "GET / " in request_str or "GET /HTTP" in request_str:
            # Handle Actual Request
            try:
                raw_gps = gps_controller.get_data()
                # Create the dict (ensure numeric values are valid)
                response_data = {
                    "latitude": raw_gps.get("latitude", 0.0),
                    "longitude": raw_gps.get("longitude", 0.0),
                    "velocity": raw_gps.get("velocity", 0.0),
                    "satellites": raw_gps.get("satellites", 0),
                    "timestamp": raw_gps.get("timestamp", 0),
                }

                response_body = ujson.dumps(response_data)

                writer.write(b"HTTP/1.1 200 OK\r\n")
                writer.write(b"Content-Type: application/json\r\n")
                writer.write(cors_headers)
                writer.write(f"Content-Length: {len(response_body)}\r\n".encode())
                writer.write(b"Connection: close\r\n\r\n")
                writer.write(response_body.encode())
            except Exception as e:
                print(f"JSON Generation Error: {e}")
                writer.write(b"HTTP/1.1 500 Server Error\r\n")
                writer.write(cors_headers)
                writer.write(b"Connection: close\r\n\r\n")

        else:
            # Handle 404 (Must also have CORS headers or browser hides the 404)
            writer.write(b"HTTP/1.1 404 Not Found\r\n")
            writer.write(cors_headers)
            writer.write(b"Connection: close\r\n\r\n")

        await writer.drain()
        writer.close()
        await writer.wait_closed()
        gc.collect()

    except Exception as e:
        print(f"Server Error: {e}")
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass


async def main_loop() -> None:
    uasyncio.create_task(gps_controller.run())
    uasyncio.create_task(uasyncio.start_server(handle_client, "0.0.0.0", PORT))


def main():
    print("Starting Async Server on port", PORT)

    loop = uasyncio.get_event_loop()
    loop.create_task(main_loop())
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    try:
        connect_wifi()
        main()
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print("Critical Error:", e)
        time.sleep(5)
        machine.reset()
