
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

	[ driver, vegan_tract_DB ] = connect_to_vegan_tract ()

	collection = vegan_tract_DB ["goals"] 

	exception = ""
	proceeds = ""
	try:
		collection.insert_one (document)
	except Exception as E:
		show_variable ("exception:", E)
	
	driver.close ()
	
	if (exception):
		raise Exception ("The goal was not added.");
	
	return proceeds;