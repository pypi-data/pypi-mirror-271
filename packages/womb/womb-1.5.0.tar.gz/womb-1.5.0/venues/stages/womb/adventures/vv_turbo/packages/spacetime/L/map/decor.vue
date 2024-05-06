


<script>

/*
	import L_map from '@@/spacetime/L/map/decor.vue'
*/

import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default {
	mounted () {
		var mymap = L.map('map').setView([51.505, -0.09], 13);

        // Add OpenStreetMap tiles to the map
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(mymap);

        // Add a marker at a specific location
        var marker = L.marker([51.5, -0.09]).addTo(mymap);

        // Add a popup to the marker
        marker.bindPopup ("<b>Hello world!</b><br>I am a popup.").openPopup();
	}
}


</script>



<template>
    <div id="map"
		:style="{
			width: '100%',
			height: '500px'
		}"
	></div>
</template>
