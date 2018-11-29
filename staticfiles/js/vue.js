var app = new Vue({
	el: '#app',
	delimiters: ['[[', ']]'],
	data: {
		dropdown: false,
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
					subreddits: result.subreddits.split(' ').join(''),
					searchterms: result.searchterms.split(' ').join(''),
				}
			} else {
				data = {
					searchname: this.nsearchname,
					subreddits: this.nsubreddits.split(' ').join(''),
					searchterms: this.nsearchterms.split(' ').join(''),
				}
				this.nsearchname = ''
				this.nsubreddits = ''
				this.nsearchterms = ''
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