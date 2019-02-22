///
/// Definition of left-sided menu..
///

class MenuItem {
	title = ''
	ref = ''
	icon = ''
	submenu = []

	constructor(title, ref, icon, submenu) {
		this.title = title || null
		this.ref = ref || null
		this.icon = icon || null
		this.submenu = submenu || null
	}
}

export default {
	items: [
		new MenuItem('Home', '/', 'home'),
		// new MenuItem('')
		new MenuItem('About', '/about', 'about-outline ')
	]
}
