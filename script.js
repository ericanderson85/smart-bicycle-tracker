const API_URL = "http://localhost:5001";
const UPDATE_INTERVAL_MS = 1000;
const INITIAL_COORDS = [42.3142, -71.042];
const INITIAL_ZOOM = 16;

const map = L.map("map").setView(INITIAL_COORDS, INITIAL_ZOOM);

L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);



let marker = L.circleMarker(INITIAL_COORDS, {
  radius: 8,          // size of dot
  color: "white",     // border color
  weight: 3,          // border thickness
  fillColor: "#007AFF",  // inside color
  fillOpacity: 1
}).addTo(map);

L.control.scale({
  position: 'bottomright',
  metric: false,
  imperial: true,
  maxWidth: 200,
}).addTo(map);


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
