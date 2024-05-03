
'''
	from vegan.adventures.monetary.DB.vegan_tract.goals.insert import insert_goals_document
	insert_goals_document (
		collection = vegan_tract_DB ["goals"],
		document = {}
	)
'''

'''
	itinerary:
		https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
		
		region = highest region number + 1
'''

from vegan.adventures.monetary.DB.vegan_tract.connect import connect_to_vegan_tract

from biotech.topics.show.variable import show_variable


def insert_goals_document (packet):
	document = packet ["document"]
	
	if ("add_region" in packet):
		add_region = packet ["add_region"]
	else:
		add_region = True

	[ driver, vegan_tract_DB ] = connect_to_vegan_tract ()

	collection = vegan_tract_DB ["goals"] 

	exception = ""
	proceeds = ""
	try:
		if (add_region):
			result = list (
				collection.aggregate ([
					{
						"$group": {
							"_id": None, 
							"max_region": {
								"$max": "$region"
							}
						}
					}
				])
			)
			region = result[0]['max_region'] + 1 if result else 1
						
			proceeds = collection.insert_one ({
				** document,
				"region": region
			}, { "unique": True })
			
		else:
			proceeds = collection.insert_one (document)
	except Exception as E:
		show_variable ("exception:", E)
	
	driver.close ()
	
	if (exception):
		raise Exception ("The goal was not added.");
	
	return proceeds;