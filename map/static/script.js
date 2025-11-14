// Inicializácia mapy so stredom na Európu
var map = L.map('map').setView([50.1109, 8.6821], 4); // [lat, lng], zoom 4 = celé kontinentálne pokrytie

// Pridanie OpenStreetMap dlaždíc
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data © OpenStreetMap contributors'
}).addTo(map);

// Tu môžeš pridať markerov z databázy ako predtým
let allHelpers=[], markers=[];

async function loadHelpers(){
    const res = await fetch("/api/helpers");
    allHelpers = await res.json();
    showMarkers();
}

function showMarkers(filter=""){
    markers.forEach(m=>map.removeLayer(m));
    markers=[];
    const filtered = allHelpers.filter(h =>
        h.meno.toLowerCase().includes(filter.toLowerCase()) || h.odbor.toLowerCase().includes(filter.toLowerCase())
    );

    filtered.forEach(h => {
    const marker = L.marker([h.lat, h.lng]).addTo(map);
    const gmapsUrl = `https://www.google.com/maps?q=${h.lat},${h.lng}`;
    marker.bindPopup(`
        <b>${h.meno}</b><br>
        ${h.odbor}<br>
        ${h.telefon? '📞 '+h.telefon+'<br>':''}
        ${h.email? '✉ '+h.email+'<br>':''}
        ${h.foto? `<img src="static/fotky/${h.foto}" style="width:100px;height:auto;"><br>` : ''}
        <a href="${gmapsUrl}" target="_blank">📍 Zobraziť v Mapách</a>
    `);
    markers.push(marker);
});
}
document.getElementById('search-box').addEventListener('input', e=>showMarkers(e.target.value));

loadHelpers();
setInterval(loadHelpers,5000); // automatická synchronizácia každých 5s