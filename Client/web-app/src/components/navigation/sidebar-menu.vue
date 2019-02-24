<template>
	<v-list dense>
		<template v-for="item in menu">
			<v-sidebar-menu-item v-if="!item.children" :key="item.id" :item="item" />
			<v-list-group v-else :key="item.id">
				<v-sidebar-menu-item
					v-for="child in item.children"
					:item="child"
					:key="child.id"
				/>
			</v-list-group>
		</template>
	</v-list>
</template>

<script>
import { VList, VListGroup } from 'vuetify/lib'

import VSidebarMenuItem from './v-sidebar-menu-item'

export default {
	name: 'v-sidebar-menu',
	components: {
		VList,
		VListGroup,
		VSidebarMenuItem
	},
	props: {
		menu: {
			type: Array,
			default: () => []
		}
	}
}
</script>

<style scoped></style>
