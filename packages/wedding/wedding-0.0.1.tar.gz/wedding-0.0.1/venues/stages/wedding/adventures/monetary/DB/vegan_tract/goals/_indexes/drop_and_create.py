

'''
	from vegan.adventures.monetary.DB.vegan_tract.goals._indexes.create import drop_and_create_goals_indexes
'''

from vegan.adventures.monetary.DB.vegan_tract.connect import connect_to_vegan_tract

def drop_and_create_goals_indexes ():
	[ driver, vegan_tract_DB ] = connect_to_vegan_tract ()

	try:
		proceeds = vegan_tract_DB ["goals"].drop_indexes ()
	except Exception as E:
		print ("exception:", E)
		
	proceeds = vegan_tract_DB ["goals"].create_index ( 
		[( "ingredients.labels", 1 )],
		
		name = "name = ingredients.labels"
	)
	
	print (f"""
	
		proceeds of index create = { proceeds }
	
	""")
	
	driver.close ()