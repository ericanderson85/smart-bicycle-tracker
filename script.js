const API_URL = "http://localhost:5001";
const UPDATE_INTERVAL_MS = 1000;
const INITIAL_COORDS = [ 42.3142, -71.042 ];
const INITIAL_ZOOM = 16;

const map = L.map("map").setView(INITIAL_COORDS, INITIAL_ZOOM);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
     maxZoom : 19,
     attribution : '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
 }).addTo(map);

let marker = L.marker(INITIAL_COORDS).addTo(map);

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const updateElementText = (elementId, text) => document.getElementById(elementId).textContent = text;

async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return await response.json();
    } catch (err) {
        console.error("Failed to fetch data:", err);
        return null;
    }
}

async function update() {
    const data = await fetchData("http://localhost:5001/");
    if (!data)
        return;

    if (data?.latitude && data?.longitude) {
        marker.setLatLng([ data.latitude, data.longitude ]);
    }

    updateElementText("latitude", `Latitude: ${data.latitude}`)
    updateElementText("longitude", `Longitude: ${data.longitude}`)
    updateElementText("velocity", `Velocity: ${data.velocity}`)
    updateElementText("battery", `Battery: ${data.battery}`)
    updateElementText("connection-status", `Connection Status: ${data.connection_status}`)
}

setInterval(update, 1000);
