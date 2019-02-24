<template>
	<v-container fill-height>
		<v-layout>
			<v-flex align-self-center md4>
				<h1 class="display4">
					Under development
				</h1>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
import { VContainer, VLayout, VFlex } from 'vuetify/lib'

export default {
	name: 'under-development',
	components: {
		VContainer,
		VLayout,
		VFlex
	},
	data() {
		return {}
	}
}
</script>
