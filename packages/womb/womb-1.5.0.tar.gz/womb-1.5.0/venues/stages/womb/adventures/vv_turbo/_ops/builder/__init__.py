

'''
	from womb.adventures.vv_turbo._ops.builder import vv_turbo_builder
	vv_turbo_builder ["on"] ()
	vv_turbo_builder ["off"] ()	
'''

'''
	objectives:
		womb adventures on --mode="pro"
		womb adventures on --mode="dev"	
'''


import womb.mixes.procedure as procedure
from womb._essence import retrieve_essence
import womb.mixes.procedure.PID as PID_monitor
	
import pathlib
from os.path import dirname, join, normpath
import sys
import os
import signal
	
this_directory = pathlib.Path (__file__).parent.resolve ()		
	

	
def _vv_turbo_builder ():
	essence = retrieve_essence ()
	
	PID_path = str (normpath (join (
		this_directory, 
		"PID.UTF8"
	)))
	
	def on ():
		the_process = procedure.demux (
			script = [
				"bun", "run", "build-monitor"
			],
			CWD = essence ["vv_turbo"] ["paths"] ["web"]
		)
		
		print ("the process:", the_process)
		print ("the process:", the_process.pid)
		
		PID_monitor.sculpt ({
			"path": PID_path,
			"PID": str (the_process.pid)
		})
		
	def off ():
		PID = PID_monitor.off ({
			"path": PID_path
		})
	
	
	
	return {
		"on": on,
		"off": off
	}
	
vv_turbo_builder = _vv_turbo_builder ()	