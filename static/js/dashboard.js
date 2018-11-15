var app = new Vue({
	el: '#app',
	delimiters: ['[[', ']]'],
	data: {
		results: null,
		loading: true,
		display: true,
		addsearch: false,
		nsearchname: '',
		nsubreddits: '',
		nsearchterms: '',

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

		},

		createsearch: function () {
			axios.post(
					'/dashboard/redditsearch/', {
						searchname: this.nsearchname,
						subreddits: this.nsubreddits,
						searchterms: this.nsearchterms,
					}
				)
				.then(() => {
					this.addsearch = false
					this.loadsearch()
				})
		}
	},
	created: function () {
		this.loadsearch()
	}

})