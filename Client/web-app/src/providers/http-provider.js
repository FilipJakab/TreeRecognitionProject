export default class HttpProvider {
	baseUrl
	axios

	constructor(axios, baseUrl) {
		this.baseUrl = baseUrl
		// trim last '/'
		// this.baseUrl = baseUrl.replace(/\/*$/g, '')
		this.axios = axios
	}

	async PostAsync(path, data, config) {
		return await this.axios.post(
			this.getPath(path), // trim '/' from start
			// `${this.baseUrl}/${path.replace(/^\/*/g, '')}`, // trim '/' from start
			data,
			config
		)
	}

	async GetAsync(path, config) {
		return await this.axios.get(this.getPath(path), config)
	}

	getPath(path) {
		return ((this.baseUrl && `${this.baseUrl}${path}`) || path).replace(
			/^\/*/g,
			''
		)
	}
}
