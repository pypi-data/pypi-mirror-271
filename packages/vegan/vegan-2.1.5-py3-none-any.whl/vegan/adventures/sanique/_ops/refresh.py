
'''
	from vegan.adventures.sanique._ops.off import turn_off_sanique
	turn_off_sanique ()
'''


'''
	sanic inspect shutdown
'''


'''
	objectives:
		[ ] implicit
'''

#----
#
from vegan._essence import retrieve_essence
from ..utilities.has_sanic_check import has_sanic_check
from .status import check_sanique_status
#
#
from biotech.topics.show.variable import show_variable
#
#
import multiprocessing
import subprocess
import time
import os
import atexit
#
#----

def background (procedure, CWD):
	show_variable ("procedure:", procedure)
	process = subprocess.Popen (procedure, cwd = CWD)


def refresh_sanique ():
	essence = retrieve_essence ()
	has_sanic_check ()

	'''
		maybe turn it on here, if it's not
	'''


	sanique_directory_path = essence ["sanique"] ["directory"]
	
	process = background (
		procedure = [
			"sanic",
			"inspect",
			"reload",
			
			f"--port",
			str (essence ["sanique"] ["inspector"] ["port"]),
		],
		CWD = sanique_directory_path
	)
	
	loop = 0
	while True:
		print ("checking sanique status")
	
		the_status = check_sanique_status ()
		if (the_status == "on"):
			break;
			
		time.sleep (1)

		loop += 1
		if (loop == 20):
			raise Exception ("Sanique doesn't seem to be turning on.")

	return;