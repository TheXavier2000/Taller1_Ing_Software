document.addEventListener("DOMContentLoaded", function() {
    var map = L.map('map').setView([4.5720763, -74.1342726], 16);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    async function loadPolygon() {
        try {
            let response = await fetch("/api/polygon");
            let data = await response.json();

            L.geoJSON(data, { style: {color: "blue"} }).addTo(map);
        } catch(error) {
            console.error("No se pudo cargar el polígono", error);
        }
    }

    async function loadTrees() {
        try {
            let response = await fetch("/api/trees");
            let data = await response.json();

            L.geoJSON(data).addTo(map);
        } catch(error) {
            console.error("No se pudieron cargar los árboles", error);
        }
    }

    document.getElementById("btnTrees").addEventListener("click", loadTrees);

    loadPolygon();
});
