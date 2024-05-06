
'''
	from womb.adventures.monetary._ops.off import turn_off_monetary_node
	mongo_process = turn_off_monetary_node ()
'''

'''
	mongod --shutdown --pidfilepath /var/run/mongodb/mongod.pid
'''

#----
#
import womb.mixes.procedure as procedure
from womb._essence import retrieve_essence
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

	#port = womb_essence ["monetary"] ["builtin_node"] ["port"]
	dbpath = essence ["monetary"] ["builtin_node"] ["path"]
	PID_path = essence ["monetary"] ["builtin_node"] ["PID_path"]
	#logs_path = womb_essence ["monetary"] ["builtin_node"] ["logs_path"]
	
	mongo_process = procedure.demux ([
		"mongod",
		"--shutdown",
		
		'--dbpath', 
		f"{ dbpath }", 
		
		"--pidfilepath",
		f"'{ PID_path }'"
	])
	
	
	
	
	return;