<template>
	<v-app>
		<v-navigation-drawer app fixed temporary v-model="drawer">
			<v-sidebar-menu :menu="menu" />
		</v-navigation-drawer>
		<v-toolbar color="indigo" dark fixed app>
			<v-toolbar-side-icon @click.stop="drawer = !drawer" />
			<v-toolbar-title>Project: Tree Recognition</v-toolbar-title>
		</v-toolbar>
		<v-content>
			<router-view></router-view>
		</v-content>
		<v-footer></v-footer>
	</v-app>
</template>

<script>
import {
	VNavigationDrawer,
	VFooter,
	VApp,
	VToolbar,
	VContent
} from 'vuetify/lib'

import VSidebarMenu from './components/navigation/sidebar-menu'
import Menu from './config/sidebar-menu.config'

export default {
	name: 'App',
	components: {
		VNavigationDrawer,
		VFooter,
		VApp,
		VToolbar,
		VContent,
		VSidebarMenu
	},
	watch: {
		$route() {
			this.drawer = !this.drawer
		}
	},
	data() {
		return {
			drawer: false,
			menu: Menu
		}
	}
}
</script>
