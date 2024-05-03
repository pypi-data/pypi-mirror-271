



#from vegan.adventures.monetary.clique import clique as monetary_clique
#from vegan.adventures.customs.clique import clique as customs_clique
#from vegan.adventures.sanique.clique import clique as sanic_clique

#----
#

#
#
from vegan.adventures._ops._clique import adventures_clique
#	
from vegan._essence import retrieve_essence
from vegan._essence import build_essence
#
#
from biotech.topics.show.variable import show_variable
#
#
import rich
import click
#
#
import os
import json
import time
import pathlib
from os.path import dirname, join, normpath
import sys
#
#----

this_directory = pathlib.Path (__file__).parent.resolve ()	

def clique ():
	'''
		Check for essence here and then set them 
		implicitly.
	'''
	#print ('essence check')
	build_essence ()

	@click.group ()
	def group ():
		pass

	#
	#	vegan on
	#
	@group.command ("print-essence")
	def print_essence ():	
		essence = retrieve_essence ()
		#rich.print_json (data = essence)
	
		
		show_variable (essence)

	@click.command ("help")
	def help ():
		import somatic
		the_mix = str (normpath (join (this_directory, "../..")))
		
		somatic.start ({
			"directory": the_mix,
			"relative path": the_mix,
			"port": 20000,
			"static port": False,
			"verbose": 1
		})

		import time
		while True:
			time.sleep (1000)
	
	
	

		
	

	

	'''
	group.add_command (on)
	group.add_command (off)
	group.add_command (refresh_op)
	group.add_command (status)
	group.add_command (print_essence)
	'''

	group.add_command (help)


	#group.add_command (monetary_clique ())
	#group.add_command (sanic_clique ())
	group.add_command (adventures_clique ())

	group ()




#
