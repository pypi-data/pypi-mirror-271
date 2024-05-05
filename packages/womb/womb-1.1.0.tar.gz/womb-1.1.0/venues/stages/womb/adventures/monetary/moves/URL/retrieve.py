
'''
	from womb.adventures.monetary.moves.URL.retrieve import retrieve_monetary_URL
'''

from womb._essence import retrieve_essence

def retrieve_monetary_URL (database = ""):
	essence = retrieve_essence ()

	if ("URL" in essence ["monetary"]):
		return essence ["monetary"] ["URL"] + database;

	return "mongodb://" + essence ["monetary"] ["builtin_node"] ["host"] + ":" + essence ["monetary"] ["builtin_node"] ["port"] + "/" + database;