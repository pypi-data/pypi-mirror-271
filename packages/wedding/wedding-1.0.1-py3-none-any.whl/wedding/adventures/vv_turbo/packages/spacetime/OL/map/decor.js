

import { methods } from './methods'

export const decor = {
	
	components: {  },
	
	data () {
		return {
			places: [],
			bounds: {
				"top": {
					"left": "",
					"right": ""
				},
				"bottom": {
					"left": "",
					"right": ""
				}
			}
		}
	},
	
	methods,
	
	mounted () {
		const map = this.draw ()
		this.map = map;
		
		map.on ('moveend', this.monitor_map_move);
		
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
				zoom: 1,
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
		
	},
	
	beforeUnmount () {
		this.map.un ('moveend', this.monitor_map_move);
		
	}
}