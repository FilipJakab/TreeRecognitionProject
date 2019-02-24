import HttpProvider from '../providers/http-provider'

export default class ImageRecognitionManager extends HttpProvider {
	constructor( axios) {
		super(axios)
	}

	async GetPredictions(images) {
		let payload = new FormData()
		images.forEach(image => payload.append('images', image))

		return (await this.PostAsync('http://localhost:5000/api/', payload, {
			headers: {
				'Content-Type': 'multipart/form-data'
			}
		})) // extracts data part of response
	}
}
