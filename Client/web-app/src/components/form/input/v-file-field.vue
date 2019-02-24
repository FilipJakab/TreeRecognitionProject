<template>
	<div>
		<v-text-field
			ref="textField"
			@click.stop="openFileDialog"
			v-bind="$props"
		/>
		<input
			type="file"
			class="hidden"
			ref="filePlaceholder"
			@change="onFileChange"
			:multiple="multiple"
		/>
		<!--<v-input v-bind="$props">
			<v-text-field @click="openFileDialog" v-bind="$props" />
		</v-input>-->
	</div>
</template>

<script>
import { VTextField } from 'vuetify/lib'

export default {
	name: 'v-file-field',
	props: ['multiple', 'label', 'placeholder'],
	components: {
		VTextField
	},
	methods: {
		onFileChange(ev) {
			this.$emit('input', ev.target.files)
		},
		openFileDialog() {
			this.$refs.textField.blur()
			this.$refs.filePlaceholder.click()
		}
	}
}
</script>

<style scoped>
.hidden {
	display: none;
}
</style>
