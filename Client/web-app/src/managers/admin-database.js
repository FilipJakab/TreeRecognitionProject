import HttpProvider from '../providers/http-provider'

export default class DatabaseManager extends HttpProvider {
	constructor(axios, baseUrl) {
		super(axios, baseUrl)
	}

	async GetTables () {
		return (await this.GetAsync('admin/database/gettables')).data
	}

	async GetTableData(tableName) {
		return (await this.GetAsync(`admin/database/${tableName}/data`, {
			params: {
				tableName
			}
		})).data
	}
}
