

'''
	mongo connection strings
		
		DB: vegan
			
			collection: 
				cautionary_ingredients
				essential_nutrients
'''


import pathlib
from os.path import dirname, join, normpath
import sys
def add_paths_to_system (paths):
	this_directory = pathlib.Path (__file__).parent.resolve ()	
	for path in paths:
		sys.path.insert (0, normpath (join (this_directory, path)))
	

add_paths_to_system ([
	'../../../../stages',
	'../../../../stages_pip'
])


#----
#
#
from vegan.adventures._ops.on import turn_on
from vegan._essence import build_essence
#
#
import biotech
#
#
import rich
#
#
import json
import pathlib
from os.path import dirname, join, normpath
import os
import sys
import subprocess
#
#----

build_essence ()
#exit ()



#----
#
name = "vegan"
this_directory = pathlib.Path (__file__).parent.resolve ()
venues = str (normpath (join (this_directory, "../../../../../venues")))
this_stage = str (normpath (join (venues, f"stages/{ name }")))

if (len (sys.argv) >= 2):
	glob_string = this_stage + '/' + sys.argv [1]
	db_directory = False
else:
	glob_string = this_stage + '/**/status_*.py'
	db_directory = normpath (join (this_directory, "DB"))

print ("glob string:", glob_string)
#
#----


os.chdir (this_directory)
build_essence ()
turn_on ()

'''
vegan_binary_path = str (normpath (join (this_directory, "../../__dictionary/vegan_1")))
subprocess.Popen (
	[ f"{ vegan_binary_path }",  "on" ],
	cwd = this_directory
)
'''

bio = biotech.on ({
	"glob_string": glob_string,
	
	"simultaneous": True,
	"simultaneous_capacity": 10,

	"time_limit": 60,

	"module_paths": [
		normpath (join (venues, "stages")),
		normpath (join (venues, "stages_pip"))
	],

	"relative_path": this_stage,
	
	"db_directory": db_directory,
	
	"aggregation_format": 2
})


bio ["off"] ()


def turn_off ():
	vegan_binary_path = str (normpath (join (this_directory, "../../__dictionary/vegan_1")))
	subprocess.Popen (
		[ f"{ vegan_binary_path }",  "off" ],
		cwd = this_directory
	)


import time
time.sleep (2)

rich.print_json (data = bio ["proceeds"] ["alarms"])
rich.print_json (data = bio ["proceeds"] ["stats"])


