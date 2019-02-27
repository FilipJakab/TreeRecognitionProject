<template>
	<v-list-tile>
		<v-list-tile-action>
			<v-icon>
				{{ item.icon }}
			</v-icon>
		</v-list-tile-action>
		<v-list-tile-content>
			<v-list-tile-title>
				<router-link :to="{ name: item.routeName }">
					{{ item.title }}
				</router-link>
			</v-list-tile-title>
		</v-list-tile-content>
	</v-list-tile>
</template>

<script>
import { MenuItem } from '../../config/sidebar-menu.config'

export default {
	name: 'v-sidebar-menu-item',
	props: {
		item: {
			type: MenuItem,
			default: null
		}
	}
}
</script>

<style scoped></style>
