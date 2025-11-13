var map = L.map('map').setView({lon: -71.0420, lat: 42.3142}, 16);

const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
maxZoom: 19,
attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
})
tiles.addTo(map);
