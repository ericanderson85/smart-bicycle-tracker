# Simple Bike Tracker Map

Displays live bike location data on a Leaflet map using an ESP32 API.

## Get the Code

```bash
git clone https://github.com/ericanderson85/smart-bicycle-tracker.git
cd smart-bicycle-tracker
```

## Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

```bash
npm install
```

## Setup ESP32

1. Connect ESP32 to USB port
2. Erase flash:

```bash
esptool erase-flash
```

3. Download micropython firmware for ESP32: https://micropython.org/download/ESP32_GENERIC/
4. Flash firmware:

```bash
esptool --baud 460800 write-flash 0x1000 /path/to/firmware.bin
```

5. Verify (should see blinking LED):

```bash
mpremote fs cp firmware/esp32/blink.py :main.py
mpremote reset
```

## Setup Environment Variables

1. Create `.env`:

```bash
cp .env.example .env
```

2. Fill in variables
3. Transfer file to ESP32:

```bash
mpremote fs cp .env :.env
```

## Run

1. Start the API on the ESP32:

```bash
mpremote fs cp firmware/esp32/main.py :main.py
mpremote reset
```

or, on local machine with sample data:

```bash
python3 -m test.run_api
```

2. Open `frontend/index.html` in your browser.
