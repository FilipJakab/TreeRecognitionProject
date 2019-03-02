import Vue from 'vue'
import VueRouter from 'vue-router'
import Axios from 'axios'

import './plugins/vuetify'
import App from './App.vue'

// vuetify css
import './assets/material-icons.css'
import './assets/fonts/roboto.css'

import { Routes } from './config/vue-router.config'

Vue.config.productionTip = false

// inject Axios to every Vue instance
Vue.prototype.$http = Axios

Vue.use(VueRouter)

new Vue({
	router: new VueRouter({
		routes: Routes
	}),
	render: h => h(App)
}).$mount('#app')
