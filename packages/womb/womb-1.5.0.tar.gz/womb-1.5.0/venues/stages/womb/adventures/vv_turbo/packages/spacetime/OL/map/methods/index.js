

import { Draw, Modify, Snap } from 'ol/interaction.js';
import Map from 'ol/Map.js';
import OSM from 'ol/source/OSM.js';
import {Vector as VectorSource} from 'ol/source.js';
import TileLayer from 'ol/layer/Tile.js';
import {Vector as VectorLayer} from 'ol/layer.js';
import View from 'ol/View.js';
import {Control, defaults as defaultControls} from 'ol/control.js';

import { get, transform, fromLonLat, toLonLat } from 'ol/proj.js';


import { getBottomLeft, getBottomRight, getTopLeft, getTopRight } from 'ol/extent';

import 'ol/ol.css';

import { Rotator_Control } from '@@/spacetime/OL/lands/controls/rotate_South'

import { rhythm_filter } from 'procedures/dates/rhythm-filter'


		

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

		this.pointer_move_RF.attempt (({ ellipse, is_last }) => {
			this.change_cursor_coordinates (event.originalEvent)
		});
	},
	
	monitor_map_move (event) {
		const component = this;
		
		// console.log ('Map moved', event);
		
		this.change_bounds_coordinates ()
	},
	
	
	
	build_map ({
		extent,
		raster,
		vector_layer
	}) {
		const map = new Map ({
			controls: defaultControls ().extend ([
				new Rotator_Control ()
			]),
			layers: [ 
				raster, 
				vector_layer 
			],
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
	
	interact () {
		
	},
	
	draw () {
		const component = this;
		
		const raster = this.receive_raster ()
		const extent = this.receive_extent ()

		const themes = {
			circles: {
				line: 'rgb(213, 143, 198, 0.8)',
				center: 'rgb(213, 143, 198, 0.5)'
			}
		}

		const vector_source = new VectorSource ();
		const vector_layer = new VectorLayer ({
			source: vector_source,
			style: {
				'fill-color': 'rgba(255, 255, 255, 0.4)',
				
				'stroke-color': '#ff50b3a6',
				'stroke-width': 4,
				
				'circle-radius': 40,
				'circle-fill-color': themes.circles.center,
				'circle-stroke-color': themes.circles.line,
				'circle-stroke-width': 8,
			}
		});
		
		const vector_glamor_layer = new VectorLayer ({
			source: new VectorSource (),
			sstyle: {
				'stroke-color': 'black',
				'stroke-width': 2,
				'fill-color': 'pink'
			},
		})


		const map = this.build_map ({
			extent,
			raster,
			vector_layer
		})
		const modify = new Modify ({
			source: vector_source
		});
		
		map.addInteraction (modify);

		let draw;
		let snap;
		const type_select = document.getElementById ('type');

		function addInteractions() {
			draw = new Draw ({
				type: type_select.value,
				source: vector_source,
				trace: true,
				traceSource: vector_layer.getSource (),
				style: {
					'stroke-color': 'pink',
					'stroke-width': 1.5,
					
					'fill-color': 'pink',
					
					'circle-radius': 6,
					'circle-fill-color': themes.circles.center,
					'circle-stroke-color': themes.circles.line,
					'circle-stroke-width': 2,
				}
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
				source: vector_source,
				style: {
					'stroke-color': 'pink',
					'stroke-width': 1.5,
					
					'fill-color': 'pink',
					
					'circle-radius': 6,
					'circle-fill-color': themes.circles.center,
					'circle-stroke-color': themes.circles.line,
					'circle-stroke-width': 2,
				}
			});
			
			map.addInteraction (snap);
		}

		/**
		 * Handle change event.
		 */
		type_select.onchange = function () {
			console.log ('onchange')
			
			map.removeInteraction (draw);
			map.removeInteraction (snap);
			
			addInteractions ();
		};

		addInteractions ();

		return map;
	}
	
}