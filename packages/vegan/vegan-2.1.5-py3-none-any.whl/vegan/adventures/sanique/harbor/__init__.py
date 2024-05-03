

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
#
from .addresses.besties__food_USDA__nature_v2__FDC_ID import besties__food_USDA__nature_v2__FDC_ID
from .addresses.besties__supp_NIH__nature_v2__DSLD_ID import besties__supp_NIH__nature_v2__DSLD_ID

#
from vegan._essence import retrieve_essence, build_essence
from vegan.adventures.alerting import activate_alert
from vegan.adventures.alerting.parse_exception import parse_exception
#
from vegan.adventures.monetary.DB.vegan_tract.goals.retrieve_one import retrieve_one_goal

from vegan.besties.supp_NIH.nature_v2._ops.retrieve import retrieve_parsed_NIH_supp
from vegan.shows_v2.recipe._ops.retrieve import retrieve_recipe
from vegan.shows_v2.recipe_with_goals._ops.formulate import formulate_recipe_with_goals	
#
#
from biotech.topics.show.variable import show_variable
#
#
import sanic
from sanic import Sanic
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
	USDA_food_ellipse = os.environ.get ('USDA_food')
	NIH_supp_ellipse = os.environ.get ('NIH_supp')
	inspector_port = os.environ.get ('inspector_port')
	essence = os.environ.get ('essence')
	
	env_vars = os.environ.copy ()
	#print ("env_vars:", env_vars)
	#show_variable () 
	
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
	
	
	#app.blueprint(swagger_blueprint)

	@app.route ("/")
	async def home (request):
		essence = retrieve_essence ()
	
		#print ("essence:", essence)
	
		return sanic.json (
			json.loads (env_vars ["essence"])
		)
	
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
	

	
	@app.get ('/goals/<region>')
	@openapi.summary ("goals")
	@openapi.description ("goals")
	async def goals_by_region (request, region):
		try:
			ingredient_doc = retrieve_one_goal ({
				"region": region
			})
			
			return sanic_response.json (ingredient_doc)
			
		except Exception as E:
			show_variable (str (E))
			
		return sanic_response.json ({
			"anomaly": "An unaccounted for anomaly occurred."
		}, status = 600)
	
	'''
		 https://sanic.dev/en/plugins/sanic-ext/openapi/decorators.html#ui
	'''
	@app.patch ('/shows_v2/recipe')
	@openapi.summary ("recipe")
	@openapi.description ("""
	
		{ 
			"IDs_with_amounts": [
				{
					"DSLD_ID": "276336",
					"packets": 10
				},
				{
					"DSLD_ID": "214893",
					"packets": 20
				},
				{
					"FDC_ID": "2412474",
					"packets": 20
				}
			] 
		}
		
	""")
	@openapi.body({
		"application/json": {
			"properties": {
				"IDs_with_amounts": { "type": "list" }
			}
		}
	})
	#@doc.produces ({'message': str})
	#@doc.response (200, {"message": "Hello, {name}!"})
	async def recipe (request):
		data = request.json
	
		show_variable ({
			"data": data
		}, mode = "pprint")
	
		try:
			recipe_packet = retrieve_recipe ({
				"IDs_with_amounts": data ["IDs_with_amounts"]
			})
			if (len (recipe_packet ["not_added"]) >= 1):
				not_found_len = len (recipe_packet ["not_added"]);
				assert (type (not_found_len) == int)
			
				not_found_len = str (not_found_len)
			
				return sanic_response.json ({
					"anomaly": f"{ not_found_len } could not be found."
				}, status = 600)
			
			assert (len (recipe_packet ["not_added"]) == 0)
			
			recipe_with_goals_packet = formulate_recipe_with_goals ({
				"recipe": recipe_packet ["recipe"],
				"goal_region": "2"
			})
			
			recipe = recipe_with_goals_packet ["recipe"]	
			
			return sanic_response.json (recipe_with_goals_packet ["recipe"])
			
		except Exception as E:
			print (str (E))
			
		return sanic_response.json ({
			"anomaly": "An unaccounted for anomaly occurred."
		}, status = 600)
	
	'''
		 https://sanic.dev/en/plugins/sanic-ext/openapi/decorators.html#ui
	'''
	besties__food_USDA__nature_v2__FDC_ID (
		app,
		openapi,
		USDA_food_ellipse
	)
	
	besties__supp_NIH__nature_v2__DSLD_ID (
		app,
		openapi,
		NIH_supp_ellipse
	)
	


		
	return app

