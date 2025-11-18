const API_URL = "http://localhost:5001";
const UPDATE_INTERVAL_MS = 1000;
const INITIAL_ZOOM = 16;

const MAP_TILES_URL =
	"https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}";

const FALLBACK_COORDS = [42.3142, -71.042]; // fallback to umass boston coordinates if initial api call fails

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
	updateElementText(
		"connection-status",
		`Connection Status: ${data.connection_status}`
	);
}

async function startMap() {
	const data = await fetchData(API_URL);
	let initial_coords = FALLBACK_COORDS;
	if (data?.latitude != null && data?.longitude != null) {
		initial_coords = [data.latitude, data.longitude];
	}

	const map = L.map("map").setView(initial_coords, INITIAL_ZOOM);
	L.tileLayer(MAP_TILES_URL, {
		maxZoom: 19,
		attribution:
			'&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);
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
