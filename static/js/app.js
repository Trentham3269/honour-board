const app = new Vue({
  el: '#app',
  methods: {
    getWinners(){
        axios.get('/api/winners')
        .then(response => {
          this.winners = response.data;
        }).catch(function (error) {
          console.log(error);
        });
      }
    },
    mounted() {
      this.getWinners();
    },
  data: {
    headers: [
      { text: 'id', value: 'id' },
      { text: 'Title', value: 'title' },
      { text: 'First Name', value: 'first_name' },
      { text: 'Initials', value: 'initials' },
      { text: 'Last Name', value: 'last_name' }
    ],
    winners: [],
  }
})
