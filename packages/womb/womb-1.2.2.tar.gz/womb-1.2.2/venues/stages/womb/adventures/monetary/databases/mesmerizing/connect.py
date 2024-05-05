



'''	
	from womb.adventures.monetary.databases.mesmerizing.connect import connect_to_mesmerizing
	[ driver, mesmerizing_databases ] = connect_to_mesmerizing ()
	driver.close ()
'''

'''
	from womb.adventures.monetary.databases.mesmerizing.connect import connect_to_mesmerizing
	places_collection = connect_to_mesmerizing () ["places"]	
	places_collection.disconnect ()
'''




from womb.adventures.monetary.moves.URL.retrieve import retreive_monetary_URL
from womb._essence import retrieve_essence
	
import pymongo

def connect_to_mesmerizing ():
	driver = pymongo.MongoClient (retreive_monetary_URL ())

	return [
		driver,
		driver [
			retrieve_essence () ["monetary"] ["databases"] ["mesmerizing"] ["alias"]
		]
	]