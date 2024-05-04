

'''
	import wedding.mixes.procedure.PID as PID_monitor
	
	PID_monitor.sculpt ({
		"path": "",
		"PID": ""
	})
	
	PID = PID_monitor.off ({
		"path": ""
	})
'''

import os
import signal

def sculpt (packet):
	with open (packet ["path"], "w") as file:
		file.write (packet ["PID"])	

def scan (packet):
	with open (packet ["path"], "r") as file:
		content = file.read()
		
	return int (content.strip ())
		
def off (packet):
	PID = scan ({
		"path": packet ["path"]
	})
	
	os.kill (PID, signal.SIGTERM)
	os.remove (packet ["path"])		