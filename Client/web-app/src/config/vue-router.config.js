import NotFound from '../pages/not-found.vue'
import Home from '../pages/home.vue'
import About from '../pages/about.vue'

export const Routes = [
	{
		path: '/',
		name: 'home',
		component: Home
	},
	{
		path: '/about',
		name: 'about',
		component: About
	},
	{
		path: '*',
		component: NotFound
	}
]
