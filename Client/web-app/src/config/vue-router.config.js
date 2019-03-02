import Home from '../pages/home'

import AdminTemplate from '../pages/admin/admin-template'
import AdminDatabase from '../pages/admin/database'

import About from '../pages/about'
import NotFound from '../pages/not-found'

export const Routes = [
	{
		path: '/',
		name: 'home',
		component: Home,
		meta: {
			breadcrumb: ''
		}
	},
	{
		path: '/admin',
		name: 'admin',
		component: AdminTemplate,
		meta: {
			breadcrumb: 'admin'
		},
		children: [
			{
				path: 'database',
				name: 'database',
				component: AdminDatabase,
				meta: {
					breadcrumb: 'database'
				}
			}
		]
	},
	{
		path: '/about',
		name: 'about',
		component: About,
		meta: {
			breadcrumb: 'about'
		}
	},
	{
		path: '*',
		component: NotFound
	}
]
