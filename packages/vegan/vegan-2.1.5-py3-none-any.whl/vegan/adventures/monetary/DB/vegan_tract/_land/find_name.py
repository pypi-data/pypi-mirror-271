



'''
	from vegan.adventures.monetary.DB.vegan_tract._land.find_name import find_ingredient_by_name
	ingredient_doc = find_ingredient_by_name ({
		"collection": "essential_nutrients",
		"name": ""
	})
'''

'''
	itinerary:
		https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
		
		region = highest region number + 1
'''
from vegan.adventures.monetary.DB.vegan_tract.connect import connect_to_vegan_tract
	
def find_ingredient_by_name (packet = {}):
	[ driver, ingredients_DB ] = connect_to_vegan_tract ()
	
	collection = ingredients_DB [ packet ["collection"] ]
	name = packet ["name"]

	found = collection.find_one ({
		"names": name 
	}, {'_id': 0})

	driver.close ()
	
	return found;
