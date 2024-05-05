


<script>



import L_map from '@@/spacetime/L/map/decor.vue'
import OL_map from '@@/spacetime/OL/map/decor.vue'

export default {
	
	components: { L_map, OL_map }
}


</script>



<template>
    <!-- <L_map /> -->
    <OL_map 
		:style="{
			
			height: '100%',
			width: '100%'
		}"
	/>
	
</template>
