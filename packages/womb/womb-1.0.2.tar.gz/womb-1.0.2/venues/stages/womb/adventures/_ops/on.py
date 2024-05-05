

'''
	from vegan._ops.on import turn_on
	turn_on ()
'''

	
from womb.adventures.monetary._ops.on import turn_on_monetary_node
from womb.adventures.sanique._ops.on import turn_on_sanique
from womb.adventures.vv_turbo._ops.builder import vv_turbo_builder
from womb.adventures.vv_turbo._ops.dev_harbor import vv_turbo_dev_harbor
	
			
from .status import check_status
			
	
import rich


def turn_on ():	
	vv_turbo_builder ["on"] ()
	vv_turbo_dev_harbor ["on"] ()
	
	turn_on_monetary_node ()
	turn_on_sanique ()

	check_status ()	

	
