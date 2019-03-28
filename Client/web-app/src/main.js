import Vue from 'vue'
import VueRouter from 'vue-router'
import Axios from 'axios'

import './plugins/vuetify'
import App from './App.vue'
import generalMixin from './components/mixins/general-mixin'

// vuetify css
import './assets/material-icons.css'
import './assets/fonts/roboto.css'

// toastr custom css
import './assets/toastr-custom.css'

import { Routes } from './config/vue-router.config'

Vue.config.productionTip = false

// inject Axios to every Vue instance
Vue.prototype.$http = Axios

Vue.mixin(generalMixin)

Vue.use(VueRouter)

new Vue({
	router: new VueRouter({
		routes: Routes
	}),
	render: h => h(App)
}).$mount('#app')
