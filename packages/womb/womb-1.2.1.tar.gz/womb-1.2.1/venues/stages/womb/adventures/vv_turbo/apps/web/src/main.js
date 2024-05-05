import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


/*
	https://ionicframework.com/docs/intro/cdn#css-1
*/



const app = createApp(App)

app.use(router)

app.mount('#app')
