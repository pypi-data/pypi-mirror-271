
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


def turn_off_sanique ():
	essence = retrieve_essence ()
	has_sanic_check ()

	the_status = check_sanique_status ()
	if (the_status == "off"):
		show_variable ('sanique is already off')
		return

	sanique_directory_path = essence ["sanique"] ["directory"]
	
	#host = essence ["sanique"] ["inspector"] ["host"]
	#port = essence ["sanique"] ["inspector"] ["port"]
	#URL = f"http://{ host }:{ port }"
	
	process = background (
		procedure = [
			"sanic",
			"inspect",
			"shutdown",
			
			f"--port",
			str (essence ["sanique"] ["inspector"] ["port"]),
			
			
		],
		CWD = sanique_directory_path
	)
	
	loop = 0
	while True:
		show_variable ("checking sanique status")
	
		the_status = check_sanique_status ()
		if (the_status == "off"):
			break;
			
		time.sleep (1)

		loop += 1
		if (loop == 20):
			raise Exception ("Sanique doesn't seem to be turning off.")

	return;