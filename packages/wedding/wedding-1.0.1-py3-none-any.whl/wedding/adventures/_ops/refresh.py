

'''
	from wedding._ops.refresh import refresh
	refresh ()
'''

#----
#

#
#----


'''
	from wedding._ops.refresh import refresh
	refresh ()
'''

#----
#
from wedding._essence import retrieve_essence
from wedding.adventures._ops.status import check_status
from wedding.adventures.sanique._ops.refresh import refresh_sanique	
#
import rich
#
#----

def refresh ():	
	essence = retrieve_essence ()

	#if ("onsite" in essence ["monetary"]):
	#	turn_on_monetary_node ()
		
	refresh_sanique ()	
		
	check_status ()
		

