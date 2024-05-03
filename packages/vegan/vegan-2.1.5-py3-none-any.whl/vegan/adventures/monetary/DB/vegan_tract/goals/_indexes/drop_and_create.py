

'''
	from vegan.adventures.monetary.DB.vegan_tract.goals._indexes.create import drop_and_create_goals_indexes
'''

from vegan.adventures.monetary.DB.vegan_tract.connect import connect_to_vegan_tract
from vegan.adventures.alerting.parse_exception import parse_exception
from vegan.adventures.alerting import activate_alert
	
def drop_and_create_goals_indexes ():
	[ driver, vegan_tract_DB ] = connect_to_vegan_tract ()

	try:
		proceeds = vegan_tract_DB ["goals"].drop_indexes ()
	except Exception as E:
		activate_alert ("emergency", {
			"exception": parse_exception (E)
		})
		
	proceeds = vegan_tract_DB ["goals"].create_index ( 
		[( "ingredients.labels", 1 )],
		
		name = "name = ingredients.labels"
	)
	
	activate_alert ("info", {
		"proceeds of index create": proceeds
	}, mode = "pprint")
	
	driver.close ()