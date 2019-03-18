<template>
	<v-container grid-list-md text-xs-center fluid>
		<v-layout col>
			<v-flex shrink xs12 md2>
				<v-file-field v-model="imagesPayload" label="Select images" multiple types=".jpg,.jpeg,.png" />
			</v-flex>
			<v-spacer />
			<v-flex md1>
				<v-btn :loading="processing" :disabled="processing" @click="SendImages">
					Send
					<v-icon right>
						cloud_upload
					</v-icon>
				</v-btn>
			</v-flex>
		</v-layout>
		<!--Show images of current request-->
		<v-layout row wrap>
			<v-flex
				:class="gridClasses"
				v-for="image in imagePredictions"
				:key="image.id">
				<v-image-prediction :item="image" />
			</v-flex>
		</v-layout>
		<!--Show images of previous requests..-->
		<v-layout col wrap>
			<v-flex xs12 v-for="(request, index) in predictionRequestHistory" :key="index">
				<!--Visual divider-->
				<v-layout row align-center>
					<v-flex xs5>
						<v-divider />
					</v-flex>
					<v-flex xs2>
						<h4 class="display2">
							{{predictionRequestHistory.length - index}}
						</h4>
					</v-flex>
					<v-flex xs5>
						<v-divider />
					</v-flex>
				</v-layout>
				<v-layout row wrap>
					<v-flex
						:class="gridClasses"
						v-for="image in request.imagePredictions"
						:key="image.id">
						<v-image-prediction :item="image" />
					</v-flex>
				</v-layout>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
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
		imagesPayload (n) {
			console.log('images changed.. : ', n)

			for (let key in n) {
				let image = n[key]

				// prevent adding existing files..
				if (
					!(image instanceof File) ||
					this.images.map(x => x.name).indexOf(image.name) !== -1
				) continue

				this.images.push(image)
				this.imagePredictions.push(new ImagePrediction(image))
			}
		}
	},
	data () {
		return {
			gridClasses: {
				'xs12': true,
				'sm6': true,
				'md4': true,
				'lg3': true
			},
			imagesPayload: [],
			imagePredictions: [],
			images: [],
			predictions: [],
			predictionRequestHistory: [],
			httpProvider: null,
			processing: false
		}
	},
	methods: {
		async SendImages () {
			if (this.processing) return

			this.processing = true
			let requestPromise
			try {
				requestPromise = this.recognitionManager.GetPredictions(this.images)
				this.predictions = (await requestPromise).data

				this.predictionRequestHistory.splice(0, 0, {
					id: Math.floor(Math.random() * 100),
					imagePredictions: this.images.map(image => new ImagePrediction(image, this.predictions[image.name]))
				})
				
				this.imagePredictions = []
				this.images = []

				this.toastSuccess('Request was successful', 'Success')
			} catch (ex) {
				this.toastError('Error occured while processing request..', 'Error')

				console.error(ex)
			}

			this.processing = false
		}
	},
	mounted() {
		console.log('mounted')
		this.recognitionManager = new ImageRecognitionManager(this.$http, process.env.VUE_APP_BASE_ENDPOINT_URL)
	}
}
</script>
