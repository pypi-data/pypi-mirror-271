
/*
	import { Rotator_Control } from '@@/spacetime/OL/lands/controls/rotate_South'
*/

import { Control } from 'ol/control.js';


/*
	https://openlayers.org/en/latest/examples/custom-controls.html
*/
export class Rotator_Control extends Control {
	constructor (opt_options) {
		const options = opt_options || {};

		const button = document.createElement ('button');
		const element = document.createElement ('div');
		button.innerHTML = 'rotate';		
		element.className = 'rotate-north ol-unselectable ol-control';
		element.appendChild (button);

		super ({
			element: element,
			target: options.target,
		});

		button.addEventListener (
			'click', 
			this.rotate_South.bind (this), 
			false
		);
	}

	rotate_South () {
		this.getMap ().getView ().setRotation (360);
	}
}