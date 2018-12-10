var Template = `
<v-flex d-flex xs12 sm6 md4 style="min-width:390px; min-height:210px">
  <v-card color="blue" dark class="white--text" style="margin:5px">
    <v-layout row style="min-height:177px">
        <v-flex xs7  style="margin-top:auto; margin-bottom:auto">
          <v-card-title primary-title>
          <div>
            <div class="headline">{{name}}</div>
            <div>Overall Rating: {{rating}}</div>
            <div>{{university}}</div>
            <div>{{major}}</div>
            <div v-if="show_grade">Grade on this course: {{grade}}</div>
          </div>
          </v-card-title>
        </v-flex>
        <v-flex xs5 style="margin-top:auto; margin-bottom:auto">
          <v-img
            src="https://cdn.vuetifyjs.com/images/cards/halcyon.png"
            height="125px"
            contain
          ></v-img>
        </v-flex>
    </v-layout>

    <v-divider light></v-divider>
    <v-card-actions>
      <v-btn flat dark>Details</v-btn>
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
    'university',
  ],
  data: function() {
    return {
      schoolFullName: '',
    }
  },
  methods: {
    deleteThis: function() {
      this.card.is_active = false;
      //this.tutor_card.is_active = false;
      //this.$emit(this.tutor_card.index);
    }
  },
  created(){
  },
  computed: {},
  template: Template
});
