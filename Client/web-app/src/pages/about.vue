<template>
	<v-container fluid fill-heigth align-center>
		<v-layout col>
			<v-flex align-self-center shrink>
				<h1 class="display4">
					About project
				</h1>
			</v-flex>
			<v-flex>
				<p>
					This project has been created for Secondary school leaving thesis.
					On this website's home page you can select images from input and these images will be sent to its API for processing.
					Side note to processing: We store images we receive, anonymously.. Just images, nothing else. By using this application you agree
					that we have right to process your sent images the way described above..
				</p>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
export default {
	name: 'about'
}
</script>

<style scoped></style>
