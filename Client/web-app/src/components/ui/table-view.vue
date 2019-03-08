<template>
	<v-card>
		<v-card-title>
			<h5 class="display-1">
				{{tableName}}
			</h5>
			<!--<v-layout row wrap>
				<v-flex xs12 md8>
				
				</v-flex>
				<v-flex xs12 md2>
					<v-btn @click="onDeleteManyClicked" color="danger">
						Delete selected
					</v-btn>
				</v-flex>
				<v-flex xs12 md2>
					<v-btn @click="onSave">
						Save
					</v-btn>
				</v-flex>
			</v-layout>-->
		</v-card-title>
		<v-layout col wrap>
			<v-flex xs12 md12>
				<v-data-table
				:headers="headers"
				:items="items"
				:loading="isLoading"
				select-all
				v-model="selected">
					<template slot="headers" slot-scope="props">
						<th class="text-xs-left"
						v-for="header in props.headers" :key="header.value">
							{{header.text}}
						</th>
						<!--<th class="text-xs-right">
							Delete
						</th>-->
					</template>
					<template slot="items" slot-scope="props">
						<!--<td>
							<v-checkbox v-model="props.selected" primary hide-details />
						</td>-->
						<td v-for="header in headers" :key="header.value">
							{{ props.item[header.value] }}
						</td>
						<!--<td class="text-xs-right">
							<v-btn icon flat color="red" @click="onDelete(items.indexOf(props.item))">
								<v-icon>close</v-icon>
							</v-btn>
						</td>-->
					</template>
				</v-data-table>
			</v-flex>
		</v-layout>
	</v-card>
</template>

<script>
export default {
	name: 'v-table-view',
	props: [
		'tableName',
		'items',
		'isLoading'
	],
	watch: {
		selected (val) {
			this.$emit('onSelectedChanged', val)
		}
	},
	computed: {
		headers () {
			if ((this.items || {}).length === 0)
				return []
				
			let keys = Object.keys(this.items[0])
			.filter(key => this.items[0][key] !== null && !(this.items[0][key] instanceof Array))
			.map(key => [
				key,
				key[0].toLocaleUpperCase()
				+ key.slice(1).replace(/([A-Z])/g, ' $1') // divide keys where Capital letters are found
			])
			.map(valueText => ({
				text: valueText[1],
				value: valueText[0],
				sortable: true
			}))
			
			return keys
		}
	},
	data () {
		return {
			selected: []
		}
	},
	methods: {
		/*onDelete (index) {
			this.$emit('onDelete', index)
		},
		onSave () {
			this.$emit('onSave')
		},
		onDeleteManyClicked () {
			this.$emit('onDeleteManyClicked')
		}*/
	}
}
</script>

<style scoped></style>
