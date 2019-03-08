<template>
	<v-card>
		<v-img :src="imageSrc" height="200" />
		<v-card-title primary-title class="pa-1">
			<h2>{{ item.file.name }}</h2>
		</v-card-title>
		<v-card-text class="pa-0">
			<v-list dense>
				<v-list-tile v-for="predKey in orderedResultKeys" :key="predKey">
					<v-list-tile-content>
						<v-list-tile-title>
							{{ predKey }}
						</v-list-tile-title>
						<v-list-tile-sub-title>
							{{ Math.floor(item.results[predKey] * 10000) / 100 }}%
						</v-list-tile-sub-title>
					</v-list-tile-content>
				</v-list-tile>
			</v-list>
		</v-card-text>
	</v-card>
</template>

<script>
import ImagePrediction from '../../models/image-prediction'

export default {
	name: 'image-prediction',
	props: {
		item: {
			type: ImagePrediction,
			default: null
		}
	},
	computed: {
		orderedResultKeys () {
			if (!this.item.results) return []

			let keys = Object.keys(this.item.results)
			keys.sort((a, b) =>
				this.item.results[a] > this.item.results[b] ? -1 : 1
			)

			return keys
		}
	},
	data () {
		return {
			imageSrc: ''
		}
	},
	async mounted () {
		this.imageSrc = await this.item.src
	}
}
</script>

<style scoped></style>
