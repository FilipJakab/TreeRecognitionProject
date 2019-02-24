<template>
	<v-card>
		<v-img :src="imageSrc" height="200" />
		<v-card-title primary-title>
			<h3 class="headline mb-0">{{ item.file.name }}</h3>
		</v-card-title>
		<v-card-text>
			<v-list dense>
				<v-list-tile v-for="pred in item.results" :key="pred">
					<v-list-tile-content>
						<v-list-tile-title>
							{{pred}}
						</v-list-tile-title>
						<v-list-tile-sub-title>
							{{item.results[pred]}}
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
	data() {
		return {
			imageSrc: ''
		}
	},
	async mounted() {
		this.imageSrc = await this.item.src
	}
}
</script>

<style scoped></style>
