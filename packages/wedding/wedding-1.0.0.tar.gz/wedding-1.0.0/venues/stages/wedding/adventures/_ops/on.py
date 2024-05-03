

'''
	from vegan._ops.on import turn_on
	turn_on ()
'''

	
from wedding.adventures.monetary._ops.on import turn_on_monetary_node
from wedding.adventures.sanique._ops.on import turn_on_sanique
from wedding.adventures.vv_turbo._ops.builder import vv_turbo_builder
	
from .status import check_status
			
	
import rich


def turn_on ():	
	vv_turbo_builder ["on"] ()
	
	return;

	turn_on_monetary_node ()
	turn_on_sanique ()

	check_status ()	

	
