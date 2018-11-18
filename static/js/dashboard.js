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
		resultid: '',
		index: '',

	},

	methods: {
		loadsearch: function () {
			axios.get('/dashboard/redditsearch/')
				.then((response) => {
					this.loading = false
					console.log(response)
					response.data = response.data.map(function (result) {
						result.display = false
						result.edit = false
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

		createsearch: function (result) {
			let data
			if (result) {
				data = {
					searchname: result.searchname,
					subreddits: result.subreddits,
					searchterms: result.searchterms,
				}
			} else {
				data = {
					searchname: this.nsearchname,
					subreddits: this.nsubreddits,
					searchterms: this.nsearchterms,
				}
			}
			axios.post(
					'/dashboard/redditsearch/',
					data
				)
				.then(() => {
					this.addsearch = false
					this.loadsearch()
				})
		},

		editsearch: function (result, index) {
			this.deletesearch(result.id, index)
			this.createsearch(result)
		}

	},
	created: function () {
		this.loadsearch()
	}

})