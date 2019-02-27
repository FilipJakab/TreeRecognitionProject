<template>
	<v-container>
		<v-layout justify-center column>
			<v-flex shrink>
				<h1 class="display4 error--text">
					404: Not found
				</h1>
			</v-flex>
			<v-flex>
				<h4 class="display-1">
					Back to <router-link to="/">
						Home
					</router-link>
				</h4>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
export default {
	name: 'not-found',
	data () {
		return {}
	}
}
</script>
