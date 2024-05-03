






'''
	import wedding.mixes.procedure as procedure
	the_process = procedure.demux (
		script = [
		
		]
	)
'''

'''
	# task
	# adventure
	# venture
	# date
	# move
	# operation
'''

import rich
	
from fractions import Fraction
import multiprocessing
import subprocess
import time
import os
import atexit

'''
	linked:
		blocking
	
	linked, tethered, explicit, bonded
'''
def linked (script):
	the_process = subprocess.Popen (script)
	atexit.register (lambda: the_process.terminate ())
	time.sleep (5)
	
	return the_process
	
'''
	demux
		non blocking
	
	
#	unlinked
#	floating,
#	untethered,
#	implicit, unbonded
'''
def demux (
	script,
	CWD = None
):
	keys = {}
	if (type (CWD) == str):
		keys ['cwd'] = CWD

	the_process = subprocess.Popen (
		script,
		
		** keys
	)
	return the_process

def go (
	script = []
):
	mongo_process = implicit (script)
