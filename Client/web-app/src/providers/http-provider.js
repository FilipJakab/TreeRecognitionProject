export default class HttpProvider {
	baseUrl
	axios

	constructor(axios) {
		// trim last '/'
		// this.baseUrl = baseUrl.replace(/\/*$/g, '')
		this.axios = axios
	}

	async PostAsync(path, data, config) {
		return await this.axios.post(
			path.replace(/^\/*/g, ''), // trim '/' from start
			// `${this.baseUrl}/${path.replace(/^\/*/g, '')}`, // trim '/' from start
			data,
			config
		)
	}
}
