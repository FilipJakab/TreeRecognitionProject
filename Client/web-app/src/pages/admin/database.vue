<template>
	<v-container fluid class="pa-0">
		<v-layout row wrap justify-space-around>
			<v-flex xs12 md9>
				<v-table-view
					v-if="tableFromQuery"
					:table-name="tableFromQuery"
					:items="tableData"
					:is-loading="loaderIsActive"/>
				</v-flex>
			<v-flex xs12 md2 order-xs1>
				<v-card>
					<v-list>
						<v-list-tile v-for="table in tables" :key="table">
							<v-list-tile-title>
								<router-link :to="{ query: { ...$route.query, table } }">
									{{ table }}
								</router-link>
							</v-list-tile-title>
						</v-list-tile>
					</v-list>
				</v-card>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
import VTableView from '../../components/ui/table-view'

import DatabaseManager from '../../managers/admin-database'

export default {
	name: 'database',
	components: {
		VTableView
	},
	watch: {
		async '$route' (to) {
			if (!to.query.table) return

			await this.loadTableData(to)
		}
	},
	computed: {
		tableFromQuery () {
			return this.$route.query.table || ''
		},
		loaderIsActive () {
			return this.loadings !== 0
		}
	},
	data () {
		return {
			dbManager: null,
			loadings: 0, // things being loaded..
			tables: [],
			tableData: [],
			currentPage: 0
		}
	},
	methods: {
		async loadTables () {
			this.loadings++
			try {
				this.tables = await this.dbManager.GetTables()
			} catch (ex) {
				console.log(ex)
			}
			this.loadings--
		},
		async loadTableData (route) {
			let { table } = route.query
			if (!table) return

			this.loadings++
			try {
				this.tableData = await this.dbManager.GetTableData(table)
			} catch (ex) {
				console.error(ex)
			}
			this.loadings--
		}
	},
	mounted () {
		console.log('mounted')
		this.dbManager = new DatabaseManager(this.$http, process.env.VUE_APP_BASE_ENDPOINT_URL)
		this.loadTables()
		this.loadTableData(this.$route)
	}
}
</script>

<style scoped></style>
