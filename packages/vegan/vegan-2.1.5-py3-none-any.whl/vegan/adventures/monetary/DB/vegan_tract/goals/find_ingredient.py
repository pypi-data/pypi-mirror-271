
'''
	from vegan.adventures.monetary.DB.vegan_tract.goals.find_ingredient import find_goal_ingredient
	goal_ingredient = find_goal_ingredient ({
		"region": "",
		
		#
		#	The ingredient label (e.g. Biotin)
		#
		#
		"label": ""
	})
'''

#----
#
from biotech.topics.show.variable import show_variable
#
#
from vegan.adventures.monetary.DB.vegan_tract.connect import connect_to_vegan_tract
from vegan.adventures.alerting.parse_exception import parse_exception
from vegan.adventures.alerting import activate_alert	
#
#----

def find_goal_ingredient (packet):

	drive = ""
	try:
		[ driver, vegan_tract_DB ] = connect_to_vegan_tract ()
	except Exception as E:
		activate_alert ("emergency", {
			"find ingredient, driver connect exception": parse_exception (E)
		})
		
		return None;
	
	proceeds = None
	try:
		region = packet ["region"]
		label = packet ["label"]

		query = {
			'region': int (region),
			'ingredients.labels': {'$regex': label.lower (), '$options': 'i'}
		}
		revenue = vegan_tract_DB ["goals"].find_one (
			query,
			{ 'ingredients.$': 1, '_id': 0  }
		) 
		
		if (type (revenue) == dict):
			if ("ingredients" in revenue):
				if (type (revenue ["ingredients"]) == list):
					if (len (revenue ["ingredients"]) >= 1):
						proceeds = revenue ["ingredients"] [0]
		
	except Exception as E:
		activate_alert ("emergency", {
			"find ingredient exception": parse_exception (E)
		})	
			
		return None;

	try:
		driver.close ()
	except Exception as E:
		activate_alert ("emergency", {
			"find ingredient, driver close exception": parse_exception (E)
		})	
		
		return None;
	
	
	return proceeds;