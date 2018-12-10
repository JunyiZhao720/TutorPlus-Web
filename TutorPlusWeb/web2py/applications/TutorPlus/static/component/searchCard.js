var Template = `
<v-flex d-flex xs12 sm6 md4 style="min-width:390px; min-height:210px">
  <v-card dark class="white--text" style="background:#959595B0; margin:5px">
    <v-layout row style="min-height:177px">
        <v-flex xs7  style="margin-top:auto; margin-bottom:auto">
          <v-card-title primary-title>
          <div>
            <div class="headline">{{name}}</div>
            <div>Overall Rating: {{show_rating}}</div>
            <div>{{university}}</div>
            <div>{{major}}</div>
            <div v-if="show_grade">Grade on this course: {{grade}}</div>
          </div>
          </v-card-title>
        </v-flex>
        <v-flex xs5 style="margin-top:auto; margin-bottom:auto">
          <v-img
            v-bind:src="imageurl"
            height="125px"
            contain
          ></v-img>
        </v-flex>
    </v-layout>

    <v-divider light></v-divider>
    <v-card-actions>
      <v-btn flat dark v-on:click="showDetail()">Details</v-btn>
    </v-card-actions>
  </v-card>
</v-flex>
`
Vue.component('search-result-card', {
  props: [
    'show_grade',
    'grade',
    'uid',
    'major',
    'name',
    'rating',
    'imageurl',
    'university',
  ],
  data: function() {
    return {
      schoolFullName: '',
      show_rating: ''
    }
  },
  methods: {
    showDetail: function() {
      //this.card.is_active = false;
      //this.tutor_card.is_active = false;
      this.$emit('show-detail', this.uid);
    }
  },
  created(){
    if (this.rating != "N/A") {
      this.show_rating = this.rating.toFixed(2);
    } else {
      this.show_rating = this.rating;
    }
  },
  computed: {},
  template: Template
});
