

#----
#
from vegan._essence import retrieve_essence
import vegan.mixes.procedure as procedure
#
#
import click
import rich
#
#
import pathlib
from os.path import dirname, join, normpath
import sys
import os
import time
#
#----


def monetary_saves_clique ():
	@click.group ("saves")
	def group ():
		pass
	

	'''
		itinerary:
			[ ] vegan_1 adventures monetary saves export --name 2.JSON
	'''
	@group.command ("export")
	@click.option (
		'--name',
		required = True
	)
	@click.option (
		'--DB',
		default = 'vegan_tract'
	)
	def save (name, db):	
		essence = retrieve_essence ()
		
		the_exports_path = essence ["monetary"] ["saves"] ["exports"] ["path"]
		the_exports_collections = essence ["monetary"] ["collections"]
	
		print ("the_exports_path:", the_exports_path)
		print ("the_exports_collections:", the_exports_collections)
	
		already_exists = []
	
		for collection in the_exports_collections:
			export_path = str (normpath (join (the_exports_path, db, collection, name)))
			if (os.path.exists (export_path) == True):
				already_exists.append (export_path)
				continue;
			
			process_strand = [
				"mongoexport",
				"--uri",
				"mongodb://localhost:39000",
				f"--db={ db }",
				f"--collection={ collection }",
				f"--out={ export_path }"
			]
			
			print (" ".join (process_strand))	
				
			procedure.go (
				script = process_strand
			)
			
			time.sleep (1)
	
		os.system (f"chmod -R 777 '{ the_exports_path }'")
	
		rich.print_json (data = {
			"already_exists": already_exists
		})
	
	'''
		vegan_1 adventures monetary saves import --name 3.JSON
	'''
	@group.command ("import")
	@click.option ('--name', required = True)
	@click.option ('--DB', default = 'vegan_tract')
	@click.option ('--drop', help = "drop the current documents in the collection", default = True)
	def insert (name, db, drop):
		essence = retrieve_essence ()

		the_exports_path = essence ["monetary"] ["saves"] ["exports"] ["path"]
		the_exports_collections = essence ["monetary"] ["collections"]
		
		not_found = []
		for collection in the_exports_collections:
			export_path = str (normpath (join (the_exports_path, db, collection, name)))
			if (os.path.exists (export_path) != True):
				not_found.append (export_path)
				continue;

			script = [
				"mongoimport",
				"--uri",
				"mongodb://localhost:39000",
				f"--db={ db }",
				f"--collection={ collection }",
				f"--file={ export_path }"
			]
			
			if (drop):
				script.append ('--drop')
				
			print (" ".join (script))	
				
			procedure.go (
				script = script
			)
			
			time.sleep (1)
		
			
		
		rich.print_json (data = {
			"not found": not_found
		})
		
		
		
		
		
		# mongoimport --uri "mongodb://localhost:39000" --db=ingredients_2 --collection=essential_nutrients --file=essential_nutrients.1.json
	
		return;
	

	return group




#



