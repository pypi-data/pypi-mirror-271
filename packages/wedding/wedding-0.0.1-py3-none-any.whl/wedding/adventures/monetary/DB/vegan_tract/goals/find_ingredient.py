
'''
	from vegan.adventures.monetary.DB.vegan_tract.goals.find_ingredient import find_goal_ingredient
	goal_ingredient = find_goal_ingredient ({
		"region": "",
		
		#
		#	The ingredient label (e.g. Biotin)
		#
		#
		"label": ""
	})
'''
from biotech.topics.show.variable import show_variable

from vegan.adventures.monetary.DB.vegan_tract.connect import connect_to_vegan_tract

def find_goal_ingredient (packet):

	drive = ""
	try:
		[ driver, vegan_tract_DB ] = connect_to_vegan_tract ()
	except Exception as E:
		show_variable ("find ingredient, driver connect exception:", E)
		return None;
	
	try:
		region = packet ["region"]
		label = packet ["label"]

		query = {
			'region': int (region),
			'ingredients.labels': {'$regex': label.lower (), '$options': 'i'}
		}
		proceeds = vegan_tract_DB ["goals"].find_one (
			query,
			{ 'ingredients.$': 1, '_id': 0  }
		) ["ingredients"] [0]
	except Exception as E:
		show_variable ("find ingredient exception:", E)
		return None;

	#rich.print_json (data = proceeds)
	try:
		driver.close ()
	except Exception as E:
		show_variable ("find ingredient, driver close exception:", E)
		return None;
	
	
	return proceeds;