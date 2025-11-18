const API_URL = "http://localhost:5001";
const UPDATE_INTERVAL_MS = 1000;
const FALLBACK_COORDS = [42.3142, -71.042]; // fallback to umass boston coordinates if initial api call fails
const INITIAL_ZOOM = 20;

// prettier-ignore
const MAP_TILE_STYLES = {
	ESRI_WORLD_IMAGERY: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
	ESRI_WORLD_STREETMAP: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
	OSM_STANDARD: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
	CARTO_LIGHT: "https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",
	CARTO_DARK: "https://cartodb-basemaps-a.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png",
	STADIA_SMOOTH: "https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png",
	STADIA_SMOOTH_DARK: "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
};
const MAP_STYLE = "ESRI_WORLD_IMAGERY";

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
function updateElementText(elementId, text) {
	const element = document.getElementById(elementId);
	element.textContent = text;
}

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

async function update(marker) {
	const data = await fetchData(API_URL);
	if (!data) return;

	if (data.latitude != null && data.longitude != null) {
		marker.setLatLng([data.latitude, data.longitude]);
	}

	updateElementText("latitude", `Latitude: ${data.latitude}`);
	updateElementText("longitude", `Longitude: ${data.longitude}`);
	updateElementText("velocity", `Velocity: ${data.velocity}`);
	updateElementText("battery", `Battery: ${data.battery}`);
	updateElementText("connection-status", `Connection Status: ${data.connection_status}`);
}

async function startMap() {
	const data = await fetchData(API_URL);
	let initial_coords = FALLBACK_COORDS;
	if (data?.latitude != null && data?.longitude != null) {
		initial_coords = [data.latitude, data.longitude];
	}

	const map = L.map("map").setView(initial_coords, INITIAL_ZOOM);
	L.tileLayer(MAP_TILE_STYLES[MAP_STYLE], { detectRetina: true }).addTo(map);
	L.control
		.scale({
			position: "bottomright",
			metric: false,
			imperial: true,
			maxWidth: 200
		})
		.addTo(map);

	const marker = L.circleMarker(initial_coords, {
		radius: 8, // size of dot
		color: "white", // border color
		weight: 3, // border thickness
		fillColor: "#007AFF", // inside color
		fillOpacity: 1
	}).addTo(map);

	sleep(UPDATE_INTERVAL_MS); // Start by sleeping, we already fetched data and updated map
	// Update the map every `UPDATE_INTERVAL_MS` ms
	setInterval(() => update(marker), UPDATE_INTERVAL_MS);
}

startMap();
