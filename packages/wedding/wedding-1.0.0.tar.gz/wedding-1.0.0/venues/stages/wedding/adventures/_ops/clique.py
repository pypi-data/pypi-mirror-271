





from .on import turn_on
from .off import turn_off
from .refresh import refresh
from .status import check_status


import click

def adventures_clique ():
	@click.group ("adventures")
	def group ():
		pass


	
	
	#
	#	vegan on
	#
	@group.command ("on")
	def on ():		
		turn_on ()

	
	@group.command ("off")
	def off ():
		turn_off ()

	@group.command ("refresh")
	def refresh_op ():
		refresh ()

	@group.command ("status")
	def status ():
		check_status ()



	return group




#



