import HttpProvider from '../providers/http-provider'

export default class ImageRecognitionManager extends HttpProvider {
	constructor(axios, baseUrl) {
		super(axios, baseUrl)
	}

	async GetPredictions(images) {
		let payload = new FormData()
		images.forEach(image => {
			payload.append('images', image)
		})

		return (await this.PostAsync(this.baseUrl, payload, {
			headers: {
				'Content-Type': 'multipart/form-data'
			}
		})).data // extract axios's data part of response
	}
}
