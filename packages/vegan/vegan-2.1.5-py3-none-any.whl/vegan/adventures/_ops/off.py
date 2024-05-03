

'''
	from vegan._ops.off import turn_off
	turn_off ()
'''

#----
#
from vegan._essence import retrieve_essence
#
from vegan.adventures.sanique._ops.off import turn_off_sanique
from vegan.adventures.monetary._ops.off import turn_off_monetary_node
from vegan.adventures._ops.status import check_status
#
#
import time	
#	
#----

def turn_off ():	
	essence = retrieve_essence ()

	if ("onsite" in essence ["monetary"]):
		turn_off_monetary_node ()	
	
	turn_off_sanique ()
	
	
	status = check_status ()
	assert (status ["monetary"] ["local"] == "off"), status
	assert (status ["sanique"] ["local"] == "off"), status