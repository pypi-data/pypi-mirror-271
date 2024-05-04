

'''
	itinerary:
		[ ] pass the current python path to this procedure
'''


'''
	https://sanic.dev/en/guide/running/manager.html#dynamic-applications
'''

'''
	worker manager:
		https://sanic.dev/en/guide/running/manager.html
'''

'''
	Asynchronous Server Gateway Interface, ASGI:
		https://sanic.dev/en/guide/running/running.html#asgi
		
		uvicorn harbor:create
'''

'''
	Robyn, rust
		https://robyn.tech/
'''

'''
	--factory
'''

#----
#
from wedding._essence import retrieve_essence, build_essence
from wedding.adventures.alerting import activate_alert
from wedding.adventures.alerting.parse_exception import parse_exception
#
from wedding.adventures.sanique.utilities.generate_inventory_paths import generate_inventory_paths
#
#
from biotech.topics.show.variable import show_variable
#
#
import sanic
from sanic import Sanic
from sanic.response import html, file, text, raw
from sanic_ext import openapi
#from sanic_openapi import swagger_blueprint, doc
import sanic.response as sanic_response
#
#
import json
import os
import traceback
#
#----

'''
	https://sanic.dev/en/guide/running/running.html#using-a-factory
'''
def create ():
	inspector_port = os.environ.get ('inspector_port')
	essence = json.loads (os.environ.get ('essence'))
	env_vars = os.environ.copy ()
	vue_dist_path = essence ["sanique"] ["vue"] ["dist"]
	
	
	'''
		#
		#	https://sanic.dev/en/guide/running/configuration.html#inspector
		#
		INSPECTOR_PORT
	'''
	app = Sanic (__name__)
	app.extend (config = {
		"oas_url_prefix": "/docs",
		"swagger_ui_configuration": {
			"docExpansion": "list" # "none"
		}
	})
	
	#app.blueprint(swagger_blueprint)
	app.config.INSPECTOR = True
	app.config.INSPECTOR_HOST = "0.0.0.0"
	app.config.INSPECTOR_PORT = int (inspector_port)
	
	
	
	#app.static ('/assets', vue_dist_path + "/assets")	
	#app.static ('/public', vue_dist_path + "/public")	
	
	inventory_assets_paths = generate_inventory_paths (vue_dist_path + "/assets")
	inventory_public_paths = generate_inventory_paths (vue_dist_path + "/public")
	
	#app.blueprint(swagger_blueprint)

	@app.route ('/')
	async def index(request):
		return await file (
			os.path.join (
				vue_dist_path, 
				'index.html'
			)
		)
		
		
	@app.route("/public/<path:path>")
	async def public_route (request, path):	
		if (path in inventory_public_paths):
			content_type = inventory_public_paths [ path ] ["mime"]
			content = inventory_public_paths [ path ] ["content"]
		
			print ("content_type:", content_type)
		
			return raw (content, content_type=content_type)
	
		return text ("not found", status = 604)	
		
	@app.route("/assets/<path:path>")
	async def assets_route (request, path):	
		if (path in inventory_assets_paths):
			content_type = inventory_assets_paths [ path ] ["mime"]
			content = inventory_assets_paths [ path ] ["content"]
		
			return raw (content, content_type=content_type)
	
		return text ("not found", status = 604)

	@app.route ("/essence")
	async def home (request):
		essence = retrieve_essence ()
		return sanic.json (essence)
	
		#return sanic_response.text ("home")
	
	
	@app.route ("/off")
	async def off (request):
		return sanic_response.text ("not possible")
		
	
	@app.route ("/PID")
	async def PID (request):
		return sanic_response.text ("not possible")
	
	@app.websocket ('/ws')
	async def ws_handler(request, ws):
		while True:
			data = await ws.recv ()  # Receive data from the client
			await ws.send (f"Echo: {data}")  # Send the received data back to the client
	


		
	return app

