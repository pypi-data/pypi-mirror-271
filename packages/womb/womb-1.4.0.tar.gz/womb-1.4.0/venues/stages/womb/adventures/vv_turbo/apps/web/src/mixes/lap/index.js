


/*
	import { lap } from '@/mixes/lap'
	const { 
		status,
		parsed,
		proceeds
	} = await lap ({
		envelope: {
			label: ""
		}
	});
	if (status !== 200) { 
		
	}
*/



import { assert_equal } from '@/grid/assert/equal'
import { has_field } from '@/grid/object/has_field'

/*
	localStorage.setItem ("node address", "http://127.0.0.1:48938")
*/
function calc_address () {
	const node_address = localStorage.getItem ("node address")
	if (typeof node_address === "string" && node_address.length >= 1) {
		return node_address
	}

	//return "https://0.0.0.0"

	return "/"
}


var address = calc_address ()


export const lap = async function ({
	method = "PATCH",
	envelope = {}
} = {}) {
	assert_equal (has_field (envelope, "label"), true)
	assert_equal (has_field (envelope, "freight"), true)

	const proceeds = await fetch (address, {
		method,
		body: JSON.stringify (envelope)
	});
	
	try {
		const proceeds_JSON = await proceeds.json ();	
		return {			
			status: proceeds.status,
			
			parsed: "yes",			
			proceeds: proceeds_JSON
		}
	}
	catch (exception) {
		console.error (exception)		
	}
	
	
	return {
		status: proceeds.status,
		parsed: "no" 
	}
}