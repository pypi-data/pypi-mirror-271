







'''
	from vegan.adventures.monetary.DB.vegan_tract.goals.retrieve_one import retrieve_one_goal
	ingredient_doc = retrieve_one_goal ({
		"region": ""
	})
'''

'''
	objective:
		https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
		region = highest region number + 1
'''
from vegan.adventures.monetary.DB.vegan_tract.connect import connect_to_vegan_tract
	
def retrieve_one_goal (packet = {}):
	[ driver, vegan_tract_DB ] = connect_to_vegan_tract ()
	
	found = vegan_tract_DB [ "goals" ].find_one ({
		"region": int (packet ["region"]) 
	}, {'_id': 0 })

	driver.close ()
	
	return found;
