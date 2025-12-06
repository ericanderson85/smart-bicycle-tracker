import machine
import uasyncio
from libraries.micropyGPS import MicropyGPS


class GPSConfig:
    UART_PORT = 2
    BAUDRATE = 9600
    TX_PIN = 17
    RX_PIN = 16
    LOCAL_OFFSET = -5  # EST
    RX_BUF = 1024


class GPSController:
    def __init__(self):
        self._uart = machine.UART(
            GPSConfig.UART_PORT,
            baudrate=GPSConfig.BAUDRATE,
            tx=GPSConfig.TX_PIN,
            rx=GPSConfig.RX_PIN,
            rxbuf=GPSConfig.RX_BUF,
        )

        # Initialize the asyncio StreamReader wrapping the UART
        self._sreader = uasyncio.StreamReader(self._uart)  # type:ignore

        self._gps = MicropyGPS(
            local_offset=GPSConfig.LOCAL_OFFSET, location_formatting="dd"
        )

        self._state = {
            "latitude": 0.0,
            "longitude": 0.0,
            "velocity": 0.0,
            "satellites": 0,
            "timestamp": 0,
        }

    def _update_state(self):
        lat_val, lat_dir = self._gps.latitude
        lon_val, lon_dir = self._gps.longitude

        latitude: float = lat_val if lat_dir == "N" else -lat_val
        longitude: float = lon_val if lon_dir == "E" else -lon_val

        timestamp = self._gps.fix_time
        if not isinstance(timestamp, int):
            timestamp = 0

        self._state = {
            "latitude": latitude,
            "longitude": longitude,
            "velocity": self._gps.speed[1],
            "satellites": self._gps.satellites_in_use,
            "timestamp": timestamp,
        }

    def get_data(self):
        return self._state

    async def run(self):
        print("GPS Controller Started...")

        while True:
            try:
                # Yields to the scheduler until at least 1 byte is available
                data = await self._sreader.read(GPSConfig.RX_BUF)

                for byte in data:
                    stat = self._gps.update(chr(byte))
                    if stat:
                        self._update_state()

            except UnicodeError:
                pass
            except Exception as e:
                print(f"GPS Error: {e}")
                await uasyncio.sleep(1)


async def run_gps():
    gps = GPSController()
    uasyncio.create_task(gps.run())

    while True:
        print(gps.get_data())

        await uasyncio.sleep(1)


if __name__ == "__main__":
    try:
        uasyncio.run(run_gps())
    except KeyboardInterrupt:
        pass
