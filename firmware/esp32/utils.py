import machine
import uasyncio


class GPSConfig:
    UART_PORT = 2
    BAUDRATE = 9600
    TX_PIN = 17
    RX_PIN = 16


# Setup UART
gps_serial = machine.UART(
    GPSConfig.UART_PORT,
    baudrate=GPSConfig.BAUDRATE,
    tx=GPSConfig.TX_PIN,
    rx=GPSConfig.RX_PIN,
)


def nmea_to_degrees(value: str) -> float | None:
    if not value or len(value) < 4:
        return None
    deg_len = 2 if len(value.split(".")[0]) <= 4 else 3
    degrees = int(value[:deg_len])
    minutes = float(value[deg_len:])
    return degrees + minutes / 60.0


def parse_rmc(sentence: str) -> tuple[float, float] | None:
    parts = sentence.split(",")
    if len(parts) < 7 or parts[2] != "A":
        return None

    latitude_raw, north_south = parts[3], parts[4]
    longitude_raw, east_west = parts[5], parts[6]

    if not latitude_raw or not longitude_raw:
        return None

    latitude = nmea_to_degrees(latitude_raw)
    longitude = nmea_to_degrees(longitude_raw)

    if latitude is None or longitude is None:
        return None

    if north_south == "S":
        latitude = -latitude
    if east_west == "W":
        longitude = -longitude

    return latitude, longitude


async def gps_task():
    stream_reader = uasyncio.StreamReader(gps_serial)  # type:ignore

    while True:
        raw = await stream_reader.readline()
        if not raw:
            continue

        try:
            decoded = raw.decode("utf-8")
            if decoded.startswith("$GPRMC"):
                coords = parse_rmc(decoded)
                if coords:
                    print("GPS:", coords)
        except UnicodeError:
            pass


async def uptime_task():
    while True:
        await uasyncio.sleep(10)


async def main():
    await uasyncio.gather(
        gps_task(),
        uptime_task(),
    )


if __name__ == "__main__":
    uasyncio.run(main())
