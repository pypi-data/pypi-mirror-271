

import { Draw, Modify, Snap } from 'ol/interaction.js';
import Map from 'ol/Map.js';
import OSM from 'ol/source/OSM.js';
import {Vector as VectorSource} from 'ol/source.js';
import TileLayer from 'ol/layer/Tile.js';
import {Vector as VectorLayer} from 'ol/layer.js';
import View from 'ol/View.js';

import { get, transform, fromLonLat, toLonLat } from 'ol/proj.js';


import { getBottomLeft, getBottomRight, getTopLeft, getTopRight } from 'ol/extent';

import 'ol/ol.css';

export const methods = {
	receive_raster () {
		const raster = new TileLayer ({
			source: new OSM ()
		});
		
		return raster;
	},
	
	receive_extent () {
		// Limit multi-world panning to one world east and west of the real world.
		// Geometry coordinates have to be within that range.
		const extent = get ('EPSG:3857').getExtent ().slice ();
		extent[0] += extent[0];
		extent[2] += extent[2];
		
		return extent;			
	},
	
	change_cursor_coordinates (originalEvent) {
		const map = this.map;
		
		var pixel = map.getEventPixel (originalEvent);
		var geo_chords = map.getCoordinateFromPixel (pixel);
		var lonLat = toLonLat (geo_chords);
		
		this.cursor_chords = {
			"lon": lonLat [0],
			"lat": lonLat [1]
		}
	},
	
	change_bounds_coordinates () {
		const map = this.map;
		
		const extent = map.getView ().calculateExtent (map.getSize ());

		const bottomLeft = getBottomLeft (extent);
		const bottomRight = getBottomRight (extent);
		const topLeft = getTopLeft (extent);
		const topRight = getTopRight (extent);

		function LL (coordinates) {
			return transform(coordinates, 'EPSG:3857', 'EPSG:4326');
		}

		this.bounds = {
			"top": {
				"left": LL (topLeft),
				"right": LL (topRight)
			},
			"bottom": {
				"left": LL (bottomLeft),
				"right": LL (bottomRight)
			}
		}
	},
	
	monitor_pointer_move (event) {
		const component = this;
		
		console.log ('Map moved', event);
		
		this.change_cursor_coordinates (event.originalEvent)
	},
	
	monitor_map_move (event) {
		const component = this;
		
		console.log('Map moved', event);
		
		this.change_bounds_coordinates ()
	},
	
	
	
	build_map ({
		extent,
		raster,
		vector
	}) {
		const map = new Map ({
			layers: [ raster, vector ],
			target: 'map',
			view: new View ({
				// center: [  22000000, 1600000 ],
				
				center: fromLonLat ([ -50, -30 ]),
				
				zoom: 2,
				extent,
			}),
		});
		
		return map;
	},
	
	draw () {
		const component = this;
		
		const raster = this.receive_raster ()
		const extent = this.receive_extent ()

		const source = new VectorSource ();
		const vector = new VectorLayer ({
			source: source,
			style: {
				'fill-color': 'rgba(255, 255, 255, 0.4)',
				'stroke-color': '#ff50b3a6',
				'stroke-width': 4,
				'circle-radius': 7,
				'circle-fill-color': '#ff50b3a6',
			},
		});

		const map = this.build_map ({
			extent,
			raster,
			vector
		})


		const modify = new Modify ({
			source: source
		});
		
		map.addInteraction (modify);

		let draw, snap; // global so we can remove them later
		const typeSelect = document.getElementById ('type');

		function addInteractions() {
			draw = new Draw ({
				source: source,
				type: typeSelect.value,
			});
			draw.on ('drawend', function(event) {
				const feature = event.feature;
				const geometry = feature.getGeometry ();
				const coordinates = geometry.getCoordinates ();
				const lonLatCoordinates = transform (coordinates, 'EPSG:3857', 'EPSG:4326');

				console.log ({ geometry, coordinates });
				
				let parsed_coordinates = []
				
				/*
					guess that is an array of coordinates
				*/
				if (Array.isArray (coordinates [0])) {
					console.info ("multiple places received", { coordinates })
					
					const places_array = coordinates [0]
					
					for (let H = 0; H < places_array.length; H++) {
						const place = places_array [H]
						
						const tudes = transform (place, 'EPSG:3857', 'EPSG:4326');
						console.log ({ place, tudes })
						
						parsed_coordinates.push ({
							longitude: tudes [0],
							latitude: tudes [1]						
						})
					}
				}
				else if (typeof coordinates [0] === "number") {
					console.info ("1 place received")
					
					const tudes = transform (coordinates, 'EPSG:3857', 'EPSG:4326');
					
					parsed_coordinates = [{
						longitude: tudes [0],
						latitude: tudes [1]						
					}]
				}
				else {
					console.error ("The coordinates could not be parsed.")
				}
				
				
				component.places.push ({
					coordinates: parsed_coordinates
				})
				

				
			});
			
			map.addInteraction (draw);
			snap = new Snap ({
				source: source
			});
			
			map.addInteraction(snap);
		}

		/**
		 * Handle change event.
		 */
		typeSelect.onchange = function () {
			console.log ('onchange')
			
			map.removeInteraction(draw);
			map.removeInteraction(snap);
			addInteractions();
		};

		addInteractions ();

		return map;
	}
	
}