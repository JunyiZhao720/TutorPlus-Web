var Template = `
<div v-if="card.is_active" style="padding:10px; margin-bottom:30px; border-radius: 3px; box-shadow: 0px 2px 2px 0px rgba(0, 0, 0, 0.15); border: 1px solid #e0e0e0;">

  <v-autocomplete v-model="school" :items="school_list" :label="'University'" clearable>
    <v-slide-x-reverse-transition slot="append-outer" mode="out-in">
    </v-slide-x-reverse-transition>
  </v-autocomplete>

  <v-layout row wrap>

  <!--
    <v-flex xs12 sm6 md3 style="margin-right:15px">
      <v-text-field v-model="card.data.course" label="Course"></v-text-field>
    </v-flex>
    -->

    <v-autocomplete v-model="course" :items="course_list" :label="'Course'"  clearable>
      <v-slide-x-reverse-transition slot="append-outer" mode="out-in">
      </v-slide-x-reverse-transition>
    </v-autocomplete>

    <v-flex xs12 sm6 md3>
      <v-text-field v-model="card.data.grade" label="Grade"></v-text-field>
    </v-flex>
    <i class="fa fa-minus-circle" style="font-size:30px; margin:auto; margin-right:10px" v-on:click="deleteThis()"></i>
  </v-layout>
</div>
`;

Vue.component('ta-course-card', {
  /* tutorCard format:
  var card = {
    data: {
      school: this.profile_university,
      course: '',
      grade: ''
    },
    index: index,
    is_active: true
  };*/
  props: [
    'card',
    'school_list',
    'school_data',
    'school_name_dict',
  ],
  data: function() {
    return {
      grade: '',
      course: '',
      school: '',
      schoolAbbr: '',
      course_list: [],
    }
  },
  methods: {
    deleteThis: function() {
      this.card.is_active = false;
      //this.tutor_card.is_active = false;
      //this.$emit(this.tutor_card.index);
    }
  },
  watch:{
    school: function(newSchool, oldSchool) {
      if (newSchool && oldSchool) {
        this.course = '';
      }
      if (!newSchool) {
        this.course_list = [];
      } else {
        var schoolAbbr = /\(([^)]+)\)/.exec(newSchool)[1].toLowerCase();
        this.card.data.school = schoolAbbr;
        this.schoolAbbr = schoolAbbr;
        if (!(schoolAbbr in this.school_data)) {
          var that = this;
          this.$http.get("https://tutorplus-93a0f.appspot.com/download-school-fields", {params: {school_id: schoolAbbr}}).then(function (data){
            that.school_data[schoolAbbr] = data.body.school;
            var course_list = that.school_data[schoolAbbr].course_list;
            that.course_list = course_list;
            var course_name_dict = {};
            for (i = 0; i < course_list.length; i++) {
              var course_key = course_list[i].split(" - ")[0].replace(/[\s]+/g, '').toLowerCase();
              course_name_dict[course_key]= course_list[i];
            }
            that.school_data[schoolAbbr].course_name_dict = course_name_dict;
          });
        } else {
          this.course_list = this.school_data[schoolAbbr].course_list;
        }
      }
    },
    course: function(newCourse, oldCourse) {
      if (this.course) {
        this.card.data.course = this.course.split(" - ")[0].replace(/[\s]+/g, '').toLowerCase();
      } else {
        this.card.data.course = '';
      }
    }
  },
  created(){
    var schoolAbbr = this.card.data.school;
    this.schoolAbbr = schoolAbbr;
    var courseAbbr = this.card.data.course;
    if (this.schoolAbbr) {
      this.school = this.school_name_dict[schoolAbbr];
      if (!(schoolAbbr in this.school_data)) {
        var that = this;
        this.$http.get("https://tutorplus-93a0f.appspot.com/download-school-fields", {params: {school_id: this.schoolAbbr}}).then(function (data){
          that.school_data[schoolAbbr] = data.body.school;
          var course_list = that.school_data[schoolAbbr].course_list;
          that.course_list = course_list;
          var course_name_dict = {};
          for (i = 0; i < course_list.length; i++) {
            var course_key = course_list[i].split(" - ")[0].replace(/[\s]+/g, '').toLowerCase();
            course_name_dict[course_key]= course_list[i];
          }
          that.school_data[schoolAbbr].course_name_dict = course_name_dict;
          if (courseAbbr) {
            that.course = that.school_data[schoolAbbr].course_name_dict[courseAbbr];
          }
        });
      } else {
        if (courseAbbr) {
          this.course = this.school_data[schoolAbbr].course_name_dict[courseAbbr];
        }
      }
    }

  },
  computed: {},
  template: Template
});
