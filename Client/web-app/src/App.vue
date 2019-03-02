<template>
	<v-app>
		<v-navigation-drawer app fixed temporary v-model="drawer">
			<v-sidebar-menu :menu="menu" />
		</v-navigation-drawer>
		<v-toolbar color="indigo" dark fixed app>
			<v-toolbar-side-icon @click.stop="drawer = !drawer" />
			<v-toolbar-title>Project: Tree Recognition</v-toolbar-title>
			<!--<v-toolbar-items>-->
			<!--</v-toolbar-items>-->
		</v-toolbar>
		<v-content>
			<v-layout justify-center row>
				<v-flex shrink>
					<v-breadcrumbs :items="breadcrumbs" divider="/"></v-breadcrumbs>
				</v-flex>
			</v-layout>
			<router-view></router-view>
		</v-content>
		<v-footer></v-footer>
	</v-app>
</template>

<script>
import VSidebarMenu from './components/navigation/sidebar-menu'
import Menu from './config/sidebar-menu.config'

export default {
	name: 'App',
	components: {
		VSidebarMenu
	},
	computed: {
		breadcrumbs () {
			// return this.$route
		}
	},
	data () {
		return {
			drawer: false,
			menu: Menu
		}
	}
}
</script>
