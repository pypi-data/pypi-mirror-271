

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
from sanic.response import html, file
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
	
	
	app.static ('/', vue_dist_path)
	
	#inventory_paths = generate_inventory_paths (directory)
	
	#app.blueprint(swagger_blueprint)

	@app.route ('/')
	async def index(request):
		show_variable ({
			"essence": essence
		})
	
		
	
		return await file (
			os.path.join (
				vue_dist_path, 
				'index.html'
			)
		)

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

