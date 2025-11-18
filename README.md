# Simple Bike Tracker Map

Displays live bike location data on a Leaflet map using a Python API.

## Get the Code

```bash
git clone https://github.com/ericanderson85/smart-bicycle-tracker.git
cd smart-bicycle-tracker
```

## Install dependencies

```bash
npm install
```

## Run

1. Start the backend API:
    ```bash
    python app.py
    ```
2. Open `index.html` in your browser.

The map updates the marker position every second using data from  
`http://localhost:5001/`.
