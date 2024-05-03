



#
#
from .group import clique as clique_group
#
#
import click
#
#

def clique ():
	@click.group ()
	def group ():
		pass

		
	@click.command ("build")
	def example_command ():	
		print ("build")

	group.add_command (example_command)
	group.add_command (clique_group ())
	
	group ()




#
