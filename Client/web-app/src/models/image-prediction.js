export default class ImagePrediction {
	id
	file
	results
	_cachedSrc

	constructor(file, results) {
		this.id = Math.random()

		this.file = file
		this.results = results || null
	}

	get src () {
		return (
			this._cachedSrc ||
			new Promise((resolve, _) => {
				let reader = new FileReader()
				reader.onload = () => {
					this._cachedSrc = reader.result
					resolve(reader.result)
				}

				reader.readAsDataURL(this.file)
			})
		)
	}
}
