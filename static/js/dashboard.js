var app = new Vue({
	el: '#app',
	delimiters: ['[[', ']]'],
	data: {
		results: null,
		loading: true,

	},

	methods: {
		loadsearch: function () {
			axios.get('/dashboard/redditsearch/')
				.then((response) => {
					this.loading = false
					console.log(response)
					response.data = response.data.map(function (result) {
						result.display = false
						return result
					})
					this.results = response.data
				})
		},
		deletesearch: function (id, index) {
			axios.delete('/dashboard/delete/' + id)
				.then(() => {
					this.results.splice(index, 1)
				})

		}
	},
	created: function () {
		this.loadsearch()
	}

})