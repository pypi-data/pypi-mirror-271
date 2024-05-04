
<script>

import { decor } from './decor';
export default decor


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

.vertical-text {
	writing-mode: vertical-rl;
	text-orientation: upright;
	white-space: nowrap;
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
				top: '40px',
				left: '20px',
				width: 'calc(100% - 420px)',
				height: 'calc(100% - 80px)',
				
				
				borderRadius: '10px',
				
				boxShadow: ([
					'#d2b12f 0px 0px 18px -3px',

					'0 0 1px 5px #750c64c4 inset',
					'0 0 6px 12px #c44fc2d4 inset'
				]).join (', '),
			}"
		>
			<div id="map"
				:style="{
					position: 'absolute',
					top: '20px',
					left: '20px',
					width: 'calc(100% - 40px)',
					height: 'calc(100% - 40px)',
					
					borderRadius: '4px',
					overflow: 'hidden'
				}"
			></div>
		
			<div top-left
				:style="{
					position: 'absolute',
					top: 0,
					left: 0,
					background: 'white'
				}"
			>
				{{ bounds.top.left [0] }}
			</div>
			
			<div
				lat
				:style="{
					position: 'absolute',
					top: 0,
					left: '50%',
					transform: 'translateX(-50%)',
					
					background: 'white'
				}"
			>
				{{ bounds.top.left [1] }}
			</div>
			
			<div
				lat
				:style="{
					position: 'absolute',
					bottom: 0,
					left: '50%',
					transform: 'translateX(-50%)',
					
					background: 'white'
				}"
			>
				{{ bounds.bottom.left [1] }}
			</div>
			
			<div 
				top-right
				:style="{
					position: 'absolute',
					top: 0,
					right: 0,
					background: 'white'
				}"
			>
				{{ bounds.top.right [0] }}
			</div>
			

			
		</div>
		
		<div
			:style="{
				position: 'absolute',
				top: '40px',
				right: '20px',
				width: '360px',
				height: 'calc(100% - 80px)',
				borderRadius: '10px',
				padding: '10px',
				
				overflow: 'scroll',
				boxShadow: ([
					'#d2b12f 0px 0px 18px -3px',

					'0 0 1px 5px #750c64c4 inset',
					'0 0 6px 12px #c44fc2d4 inset'
				]).join (', '),
				background: 'white'
			}"
		>
			<ul
				:style="{
					padding: '5px'
				}"
			>
				<li 
					v-for="place in places"
					:style="{
						'list-style-type': 'none',
						border: '2px solid #ddd',
						marginBottom: '5px'
					}"
				>
					<div>
						<h2>names: </h2>					
						<p v-for="name in place ['names']">
							{{ name }}
						</p>
					</div>
				
					<div>
						<h2>notes: </h2>					
						<p v-for="note in place ['notes']">
							{{ note }}
						</p>
					</div>

					<table>
						<thead>
							<th>lat</th>
							<th>lon</th>
						</thead>
						<tbody>
							<tr v-for="coordinate in place ['coordinates']">
								<td>{{ coordinate ["latitude"] }}</td>
								<td>{{ coordinate ["longitude"] }}</td>
							</tr>
						</tbody>						
					</table>
				</li>
			</ul>
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