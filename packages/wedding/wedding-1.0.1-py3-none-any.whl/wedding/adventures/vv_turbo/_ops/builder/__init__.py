

'''
	from wedding.adventures.vv_turbo._ops.builder import vv_turbo_builder
	vv_turbo_builder ["on"] ()
	vv_turbo_builder ["off"] ()	
'''

'''
	objectives:
		wedding adventures on --mode="pro"
		wedding adventures on --mode="dev"	
'''


import wedding.mixes.procedure as procedure
from wedding._essence import retrieve_essence
import wedding.mixes.procedure.PID as PID_monitor
	
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