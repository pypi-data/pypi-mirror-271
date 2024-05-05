<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
	<nav
		:style="{
			boxSizing: 'border-box',
			height: '60px',
			width: '100%',
			padding: '10px 0'
		}"
	>
		<RouterLink to="/">Home</RouterLink>
		<RouterLink to="/about">About</RouterLink>
	</nav>

	<div
		:style="{
			position: 'relative',
			height: 'calc(100vh - 60px)'
		}"
	>
		<RouterView />
	</div>
</template>

<style scoped>

</style>
