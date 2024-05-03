

'''
import vegan.monetary.ingredients.DB.on as ingredient_DB_on
import vegan.monetary.ingredients.DB.off as ingredient_DB_off
import vegan.monetary.ingredients.DB.status as ingredient_DB_status
import vegan.monetary.ingredients.DB.connect as connect_to_ingredient

'''

#----
#
#	local node toggle
#
from .on import turn_on_monetary_node
from .off import turn_off_monetary_node
#
#	local or remote 
#
from .status import check_monetary_status
#
from .saves._clique import monetary_saves_clique
#
#
import click
#
#----

def monetary_clique ():
	@click.group ("monetary")
	def group ():
		pass


	@group.command ("on")
	#@click.option ('--example-option', required = True)
	def on ():
		print ("on")
		mongo_process = turn_on_monetary_node ()

	@group.command ("off")
	#@click.option ('--example-option', required = True)
	def off ():
		turn_off_monetary_node ()

	@group.command ("status")
	#@click.option ('--example-option', required = True)
	def off ():
		check_monetary_status (
			loop_limit = 3
		)


	group.add_command (monetary_saves_clique ())

	return group




#



