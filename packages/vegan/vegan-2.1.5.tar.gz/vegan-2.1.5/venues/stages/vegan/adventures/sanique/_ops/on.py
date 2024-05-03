

'''
	from vegan.adventures.sanique._ops.on as turn_on_sanique
	turn_on_sanique ()
'''

'''
	python3 --shutdown --pidfilepath /var/run/mongodb/mongod.pid
'''

'''
	sanic /vegan/venues/stages/vegan/adventures/sanique/harbor/on.proc.py
'''

#----
#
#
from ..utilities.has_sanic_check import has_sanic_check
from .status import check_sanique_status
#
from vegan._essence import retrieve_essence
#
#
from biotech.topics.show.variable import show_variable
#
#
import atexit
import json
import multiprocessing
import subprocess
import time
import os
import shutil
import sys
import time
#
#----


	

def floating_process (procedure, CWD, env):
	show_variable ("procedure:", procedure)
	process = subprocess.Popen (
		procedure, 
		cwd = CWD,
		env = env
	)
	
	pid = process.pid
	
	show_variable ("sanic pid:", pid)

def turn_on_sanique (packet = {}):
	essence = retrieve_essence ()

	has_sanic_check ()

	the_status = check_sanique_status ()
	if (the_status == "on"):
		show_variable ("sanic is already on")		
		return;

	harbor_port = essence ["sanique"] ["port"]
	harbor_path = essence ["sanique"] ["directory"]

	env_vars = os.environ.copy ()
	env_vars ["USDA_food"] = essence ["USDA"] ["food"]
	env_vars ["NIH_supp"] = essence ["NIH"] ["supp"]
	env_vars ['inspector_port'] = essence ["sanique"] ["inspector"] ["port"]
	env_vars ['PYTHONPATH'] = ":".join (sys.path)
	
	env_vars ['essence'] = json.dumps (retrieve_essence ())

	process = floating_process (
		procedure = [
			"sanic",
			f'harbor:create',
			f'--port={ harbor_port }',
			f'--host=0.0.0.0',
			
			'--fast',
			'--factory',
			
			#'--dev'
		],
		CWD = harbor_path,
		env = env_vars
	)
	
	
	loop = 0
	while True:
		show_variable ("checking sanique status")
	
		the_status = check_sanique_status ()
		if (the_status == "on"):
			break;
		
		time.sleep (1)

		loop += 1
		if (loop == 20):
			raise Exception ("Sanique doesn't seem to be turning on.")

	return;