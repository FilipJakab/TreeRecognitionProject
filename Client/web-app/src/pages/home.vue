<template>
	<v-container grid-list-md text-xs-center fluid>
		<v-layout row wrap>
			<v-flex xs12 md10>
				<v-file-field v-model="imagesPayload" label="Select images" multiple />
			</v-flex>
			<v-flex md1 offset-md1>
				<v-btn
				:loading="processing"
				:disabled="processing"
				@click="SendImages">
					Send
					<v-icon right>
						cloud_upload
					</v-icon>
				</v-btn>
			</v-flex>
		</v-layout>
		<v-layout row wrap v-for="imagesRow in imagesMatrix" :key="imagesRow[0]">
			<v-flex
				xs12
				:class="imagesFlexClasses"
				v-for="image in imagesRow[1]"
				:key="image.id"
			>
				<v-image-prediction :item="image" />
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
import Axios from 'axios'

import VFileField from '../components/form/input/v-file-field'

import VImagePrediction from '../components/ui/image-prediction'
import ImagePrediction from '../models/image-prediction'

import ImageRecognitionManager from '../managers/image-recognition-manager'

export default {
	name: 'home',
	components: {
		VFileField,
		VImagePrediction
	},
	watch: {
		imagesPayload(n) {
			console.log('images changed.. : ', n)

			for (let key in n) {
				let image = n[key]

				// prevent adding existing files..
				if (!(image instanceof File) || this.images.indexOf(image) !== -1)
					continue

				this.images.push(image)
				this.imagePredictions.push(new ImagePrediction(image))
			}
		}
	},
	computed: {
		imagesFlexClasses() {
			let res = {}
			res['md' + Number(12 / this.imagesPerRow)] = true
			return res
		},
		imagesMatrix() {
			let rows = []

			for (
				let i = 0;
				i < Math.ceil(this.imagePredictions.length / this.imagesPerRow);
				i++
			) {
				rows.push([
					Math.random(),
					this.imagePredictions.slice(
						i * this.imagesPerRow,
						(i + 1) * this.imagesPerRow
					)
				])
			}

			return rows
		}
	},
	data() {
		return {
			imagesPerRow: 3,
			imagesPayload: [],
			imagePredictions: [],
			images: [],
			predictions: [],
			httpProvider: null,
			processing: false
		}
	},
	methods: {
		async SendImages() {
			if (this.processing)
				return
			
			this.processing = true
			try {
				this.predictions = await this.recognitionManager.GetPredictions(
					this.images
				)
				
				console.log(this.predictions)
			}
			finally {
				this.processing = false
			}
		}
	},
	mounted() {
		this.recognitionManager = new ImageRecognitionManager(Axios/*.create({
			baseURL: process.env.VUE_APP_BASE_ENDPOINT_URL,
			withCredentials: false,
			headers: {
				'Content-Type': 'application/json'
			}
		})*/)
	}
}
</script>
