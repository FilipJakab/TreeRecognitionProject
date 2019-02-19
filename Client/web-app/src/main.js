import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'

// vuetify css
import './assets/material-icons.css'
import './assets/fonts/roboto.css'

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
