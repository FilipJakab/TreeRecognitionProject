/// Definition of left-sided menu..

export class MenuItem {
	id = null
	title = ''
	routeName = ''
	icon = ''
	children = []

	constructor(title, routeName, icon, children) {
		this.id = Math.random()

		this.title = title || null
		this.routeName = routeName || null
		this.icon = icon || null
		this.children = children || null
	}
}

export default [
	new MenuItem('Home', 'home', 'home'),
	new MenuItem('Admin', 'admin', 'person'),
	new MenuItem('About', 'about', 'about-outline')
]
