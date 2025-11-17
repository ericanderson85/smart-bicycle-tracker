const API_URL = "http://localhost:5001";
const UPDATE_INTERVAL_MS = 1000;
const INITIAL_COORDS = [42.3142, -71.042];
const INITIAL_ZOOM = 16;

const map = L.map("map").setView(INITIAL_COORDS, INITIAL_ZOOM);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

let marker = L.marker(INITIAL_COORDS).addTo(map);

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

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

async function updateUI() {
  const data = await fetchData("http://localhost:5001/");
  if (!data) return;

  document.getElementById("latitude").textContent = `Latitude: ${data.latitude}`;
  document.getElementById("longitude").textContent = `Longitude: ${data.longitude}`;
  document.getElementById("velocity").textContent = `Velocity: ${data.velocity}`;
  document.getElementById("battery").textContent = `Battery: ${data.battery}`;
  document.getElementById("connection-status").textContent = `Connection Status: ${data.connection_status}`;
}

async function updateMarkerLoop() {
  while (true) {
    const data = await fetchData(API_URL);

    if (data?.latitude && data?.longitude) {
      marker.setLatLng([data.latitude, data.longitude]);
    }

    await sleep(UPDATE_INTERVAL_MS);
  }
}

updateMarkerLoop();
setInterval(updateUI, 1000); 

