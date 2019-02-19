<template>
	<v-app>
		<v-navigation-drawer app
		fixed
		v-model="drawer">
			<v-list dense>
				<v-list-tile>
					<v-list-tile-action>
						<v-icon>home</v-icon>
					</v-list-tile-action>
					<v-list-tile-content>
						<v-list-tile-title>Home</v-list-tile-title>
					</v-list-tile-content>
				</v-list-tile>
				
			</v-list>
		</v-navigation-drawer>
		<v-toolbar color="indigo" dark fixed app>
			<v-toolbar-side-icon @click.stop="drawer = !drawer" />
			<v-toolbar-title></v-toolbar-title>
		</v-toolbar>
		<v-footer></v-footer>
	</v-app>
</template>

<script>
	import {
		VNavigationDrawer,
		VFooter,
		VApp,
		VList,
		VIcon,
		VToolbar
	} from 'vuetify/lib'
	
	export default {
		name: 'App',
		components: {
			VNavigationDrawer,
			VFooter,
			VApp,
			VList,
			VIcon,
			VToolbar
		},
		data () {
			return {
				drawer: null
			}
		}
	}
</script>
