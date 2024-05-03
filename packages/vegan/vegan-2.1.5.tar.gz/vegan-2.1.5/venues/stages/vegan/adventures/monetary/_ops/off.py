
'''
	from vegan.monetary.ingredients.DB.off import turn_off_monetary_node
	mongo_process = turn_off_monetary_node ()
'''

'''
	mongod --shutdown --pidfilepath /var/run/mongodb/mongod.pid
'''

#----
#
import vegan.mixes.procedure as procedure
from vegan._essence import retrieve_essence
#
#
import multiprocessing
import subprocess
import time
import os
import atexit
#
#----


def turn_off_monetary_node (
	exception_if_off = False
):
	essence = retrieve_essence ()

	#port = vegan_essence ["monetary"] ["onsite"] ["port"]
	dbpath = essence ["monetary"] ["onsite"] ["path"]
	PID_path = essence ["monetary"] ["onsite"] ["PID_path"]
	#logs_path = vegan_essence ["monetary"] ["onsite"] ["logs_path"]
	
	mongo_process = procedure.implicit ([
		"mongod",
		"--shutdown",
		
		'--dbpath', 
		f"{ dbpath }", 
		
		"--pidfilepath",
		f"'{ PID_path }'"
	])
	
	
	
	
	return;