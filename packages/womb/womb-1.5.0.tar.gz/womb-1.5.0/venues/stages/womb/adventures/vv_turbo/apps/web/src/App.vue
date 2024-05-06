<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
	<main>
		<nav
			:style="{
				boxSizing: 'border-box',
				height: '60px',
				width: '100%',
				padding: '10px 20px',
				background: 'linear-gradient(22deg, #d58fc6, #dd8edd)',
				display: 'flex'
			}"
		>
			<RouterLink 
				:style="{ 
					color: '#6c0d6c', 
					margin: '0 20px', 
					padding: '6px 10px' ,
					borderRadius: '4px'
				}" 
				to="/"
			>Home</RouterLink>
			<RouterLink 
				:style="{ 
					color: '#6c0d6c', 
					margin: '0 20px', 
					padding: '6px 10px' ,
					borderRadius: '4px'
				}" 
				to="/about"
			>About</RouterLink>
		</nav>

		<div
			:style="{
				position: 'relative',
				height: 'calc(100vh - 60px)',
				background: 'linear-gradient(22deg, #d58fc6, #dd8edd)'
			}"
		>
			<RouterView />
		</div>
	</main>
</template>

<style scoped>

</style>
