


'''
	
'''

import os

def seek_essence ():
	CWD = os.getcwd ()
	
	the_name = "wedding_essence.py"
	
	found_essence_path = False
	possible_directory = CWD	
	while True:
		possible_location = str (normpath (join (possible_directory, the_name)));
		print ("checking for essence:", possible_location)
		
		if os.path.exists (possible_location):
			found_essence_path = possible_location
			print ("essence found @:", possible_location)
			break;
			
		possible_directory = os.path.dirname (possible_directory)
			
		if (possible_directory == "/"):
			break;
			
			
	if (type (found_essence_path) != str):
		raise Exception (f"{ the_name } not found")
		
	return possible_directory
			