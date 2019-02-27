<template>
	<v-container fluid>
		<v-layout row wrap>
			<v-flex xs12 md2>
				<!--Move to separate config file-->
				<v-card>
					<v-list>
						<v-list-tile>
							<v-list-tile-content>
								<v-list-tile-title>
									<span v-if="$route.name === 'database'">
										Database tables
									</span>
									<router-link v-else :to="{ name: 'database' }">
										Database tables
									</router-link>
								</v-list-tile-title>
							</v-list-tile-content>
						</v-list-tile>
					</v-list>
				</v-card>
			</v-flex>
			<v-flex xs12 md10>
				<router-view></router-view>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
import DatabaseManager from '../../managers/admin-database'

export default {
	name: 'admin-template'
}
</script>

<style scoped></style>
