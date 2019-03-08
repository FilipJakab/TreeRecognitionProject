<template>
	<v-app>
		<v-navigation-drawer app fixed temporary v-model="drawer">
			<v-sidebar-menu :menu="menu" />
		</v-navigation-drawer>
		<v-toolbar color="indigo" dark fixed app>
			<v-toolbar-side-icon @click.stop="drawer = !drawer" />
			<v-toolbar-title>Project: Tree Recognition</v-toolbar-title>
			<v-toolbar-items>
				<v-breadcrumbs :items="breadcrumbs" divider="/" dark>
					<template slot="item" slot-scope="props">
						<span v-if="props.item.disabled">
							{{props.item.text}}
						</span>
						<router-link v-else :to="props.item.href" class="white--text">
							{{props.item.text}}
						</router-link>
					</template>
				</v-breadcrumbs>
			</v-toolbar-items>
		</v-toolbar>
		<v-content>
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
			let { matched } = this.$route
			return matched.map(route => ({
				text: route.meta.breadcrumb,
				disabled: matched.indexOf(route) == (matched.length - 1),
				href: route.path
			}))
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
