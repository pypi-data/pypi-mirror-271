
<script>

import {Draw, Modify, Snap} from 'ol/interaction.js';
import Map from 'ol/Map.js';
import OSM from 'ol/source/OSM.js';
import {Vector as VectorSource} from 'ol/source.js';
import TileLayer from 'ol/layer/Tile.js';
import {Vector as VectorLayer} from 'ol/layer.js';
import View from 'ol/View.js';

import {get} from 'ol/proj.js';

import 'ol/ol.css';


export default {
	
	methods: {
		receive_raster () {
			const raster = new TileLayer({
				source: new OSM ()
			});
			
			return raster;
		},
		
		receive_extent () {
			const extent = get('EPSG:3857').getExtent().slice();
			extent[0] += extent[0];
			extent[2] += extent[2];
			
			return extent;			
		},
		
		draw () {
			const raster = this.receive_raster ()

			const source = new VectorSource();
			const vector = new VectorLayer({
			  source: source,
			  style: {
				'fill-color': 'rgba(255, 255, 255, 0.2)',
				'stroke-color': '#ffcc33',
				'stroke-width': 2,
				'circle-radius': 7,
				'circle-fill-color': '#ffcc33',
			  },
			});

			// Limit multi-world panning to one world east and west of the real world.
			// Geometry coordinates have to be within that range.
			const extent = get('EPSG:3857').getExtent().slice();
			extent[0] += extent[0];
			extent[2] += extent[2];
			const map = new Map({
			  layers: [raster, vector],
			  target: 'map',
			  view: new View({
				center: [-11000000, 4600000],
				zoom: 4,
				extent,
			  }),
			});

			const modify = new Modify({source: source});
			map.addInteraction(modify);

			let draw, snap; // global so we can remove them later
			const typeSelect = document.getElementById('type');

			function addInteractions() {
			  draw = new Draw({
				source: source,
				type: typeSelect.value,
			  });
			  map.addInteraction(draw);
			  snap = new Snap({source: source});
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

			addInteractions();

			return map;
		}
		
	},
	
	mounted () {
		const draw = this.draw ()
		
		/*
		const layers_1 = [
			new TileLayer({
				source: new OSM(),
			}),
		]
		const map = new Map({
			layers: [raster, vector],

			target: 'map',
			view: new View ({
				center: [0, 0],
				zoom: 2,
			}),
		});
		*/
		
		document.getElementById('zoom-out').onclick = function () {
			const view = map.getView();
			const zoom = view.getZoom();
			view.setZoom(zoom - 1);
		};

		document.getElementById('zoom-in').onclick = function () {
			const view = map.getView();
			const zoom = view.getZoom();
			view.setZoom(zoom + 1);
		};
		
	}
}

</script>

<style scoped>

a.skiplink {
	position: absolute;
	clip: rect(1px, 1px, 1px, 1px);
	padding: 0;
	border: 0;
	height: 1px;
	width: 1px;
	overflow: hidden;
}
a.skiplink:focus {
	clip: auto;
	height: auto;
	width: auto;
	background-color: #fff;
	padding: 0.3em;
}
#map:focus {
	outline: #4A74A8 solid 0.15em;
}

</style>

<template>
	<div
		:style="{
			position: 'absolute',
			top: 0,
			left: 0,
			width: '100%',
			height: '500px',
			
			background: 'linear-gradient(22deg, black, purple)'
		}"
	>
		<div
			:style="{
				position: 'absolute',
				top: '60px',
				left: '60px',
				width: 'calc(100% - 120px)',
				height: 'calc(100% - 120px)',
				borderRadius: '10px',
				overflow: 'hidden',
				boxShadow: '#d2b12f 0px 0px 18px -3px'
			}"
		>
			<div id="map"
				:style="{
					width: '100%',
					height: '100%'
				}"
			></div>
		</div>
		
		<div>
			<button id="zoom-out">Zoom out</button>
			<button id="zoom-in">Zoom in</button>
			
			<select id="type">
				<option value="Point">Point</option>
				<option value="LineString">LineString</option>
				<option value="Polygon">Polygon</option>
				<option value="Circle">Circle</option>
			</select>
		</div>
	</div>
</template>