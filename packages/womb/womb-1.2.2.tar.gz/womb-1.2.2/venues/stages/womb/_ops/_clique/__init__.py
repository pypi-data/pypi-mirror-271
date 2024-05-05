



#
from womb.adventures._ops.clique import adventures_clique
from womb.adventures._ops.on import turn_on
from womb.adventures._ops.off import turn_off
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

	@group.command ("on")
	def on ():		
		turn_on ()
		
	@group.command ("off")
	def off ():		
		turn_off ()

	group.add_command (example_command)
	
	group.add_command (clique_group ())
	group.add_command (adventures_clique ())
	
	group ()




#
