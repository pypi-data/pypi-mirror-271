

'''
	from vegan._ops.off import turn_off
	turn_off ()
'''

#----
#
from .status import check_status
from womb.adventures.sanique._ops.off import turn_off_sanique
from womb.adventures.monetary._ops.off import turn_off_monetary_node
from womb.adventures.vv_turbo._ops.builder import vv_turbo_builder
from womb.adventures.vv_turbo._ops.dev_harbor import vv_turbo_dev_harbor
#
import time	
#	
#----

def off (move):
	try:
		move ()
	except Exception as E:
		print ("turn off exception:", E)

def turn_off ():
	off (vv_turbo_builder ["off"])
	off (vv_turbo_dev_harbor ["off"])
	off (turn_off_sanique)
	off (turn_off_monetary_node)

	check_status ()
