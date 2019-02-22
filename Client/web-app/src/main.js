import Vue from 'vue'
import { VueRouter } from 'vue-router'

import './plugins/vuetify'
import App from './App.vue'

// vuetify css
import './assets/material-icons.css'
import './assets/fonts/roboto.css'

Vue.config.productionTip = false

Vue.use(VueRouter)

new Vue({
  render: h => h(App),
}).$mount('#app')
