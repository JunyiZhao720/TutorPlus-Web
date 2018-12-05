// This is the js for the default/index.html view.
// register modal component
Vue.component('modal', {
  template: '#modal-template'
});

//Vue.component('v-select', VueSelect.VueSelect);


var Template_TA_Course_Card = `
<div v-if="card.is_active" style="padding:10px; margin-bottom:30px; border-radius: 3px; box-shadow: 0px 2px 2px 0px rgba(0, 0, 0, 0.15); border: 1px solid #e0e0e0;">
<v-autocomplete v-model="card.data.school" :items="school_list" :label="'University'" clearable>
  <v-slide-x-reverse-transition slot="append-outer" mode="out-in">
  </v-slide-x-reverse-transition>
</v-autocomplete>

  <v-layout row wrap>
    <v-flex xs12 sm6 md3 style="margin-right:15px">
      <v-text-field v-model="card.data.course" label="Course"></v-text-field>
    </v-flex>
    <v-flex xs12 sm6 md3>
      <v-text-field v-model="card.data.grade" label="Grade"></v-text-field>
    </v-flex>
    <i class="fa fa-minus-circle" style="font-size:30px; margin:auto; margin-right:10px" v-on:click="deleteThis()"></i>
  </v-layout>
</div>
`;

Vue.component('ta-course-card', {
  props: [
    'card',
    'school_list',
    'school_data'
  ],
  data: function() {
    return {
      grade: '',
      course: '',
      school: ''
    }
  },
  methods: {
    deleteThis: function() {
      this.card.is_active = false;
      //this.tutor_card.is_active = false;
      //this.$emit(this.tutor_card.index);
    }
  },
  computed: {},
  template: Template_TA_Course_Card
});


var app = function() {

  var self = {};

  Vue.config.silent = false; // show all warnings

  // Extends an array
  self.extend = function(a, b) {
    for (var i = 0; i < b.length; i++) {
      a.push(b[i]);
    }
  };

  // Enumerates an array.
  var enumerate = function(v) {
    var k = 0;
    return v.map(function(e) {
      e._idx = k++;
    });
  };



  /*********************************************************************************************************/
  /*Login functions*/
  self.is_logged_in_listener = function() {
    console.log("User listener is online!");
    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        console.log("User listener: login!");
        // firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
        //
        //     console.log(idToken)
        //     // Send token to your backend via HTTPS
        //     // $.post(check_userId_url, {
        //     //     userId: idToken
        //     // });
        //
        // }).catch(function(error) {
        //   // Handle error
        //     const errorMessage = error.message;
        //     alert("Error : " + errorMessage);
        // });
        if (user.emailVerified == true) {
          console.log("At user listener: your email has been verified");
          console.log("The uid of the user is:", user.uid);
          self.vue.logged_in = true;
          var db = firebase.firestore();
          var user_uid = user.uid;
          var userRef = db.collection("users").doc(user_uid);
          userRef.get().then(function(doc) {
            if (doc.exists) {
              user_profile = doc.data();
              console.log("User document found");
              if (user_profile.name) {
                self.vue.profile_name = user_profile.name;
              }
              if (user_profile.university) {
                self.vue.profile_university = self.vue.school_name_dict[user_profile.university];
              }
              if (user_profile.gender) {
                self.vue.profile_gender = (user_profile.gender == 'male') ? 'Male' : 'Female';
              }
              if (user_profile.major) {
                self.vue.profile_major = user_profile.major;
              }
              if(user_profile.ps) {
                self.vue.profile_personal_statement = user_profile.ps;
              }
              self.vue.profile_email = user.email;
              db.collection("users").doc(user_uid).collection("courses").get().then(function(querySnapshot) {
                querySnapshot.forEach(function(doc) {
                  // doc.data() is never undefined for query doc snapshots
                  tutorProf = doc.data();
                  //console.log(doc.id, " => ", doc.data());
                  var index = self.vue.tutor_card_list.length;
                  var tutorCard = {
                    data: {
                      school: self.vue.school_name_dict[tutorProf.school],
                      course: tutorProf.course,
                      grade: tutorProf.grade
                    },
                    index: index,
                    is_active: true
                  };
                  self.vue.tutor_card_list.push(tutorCard);
                });
              });
            } else {
              // doc.data() will be undefined in this case
              console.log("Cannot find user doc, creating new document.");
              db.collection("users").doc(user_uid).set({
                email: user.email,
                gender: '',
                major: '',
                name: '',
                university: '',
                ps: ''
              });
            }
          });
        } else {
          console.log("At user listener: your email is not verified yet");
          self.vue.logged_in = false;
        }
      } else {
        // not logging in
        self.vue.logged_in = false;
        console.log("User listener: logout!");
      }
    });
  };

  self.is_logged_in = function() {
    let user = firebase.auth().currentUser;
    var login_state = false;

    if (user) {
      login_state = true;
    }

    self.vue.logged_in = login_state;
  };

  self.logout = function() {
    firebase.auth().signOut().then(function() {
      // Sign-out successful.
    }).catch(function(error) {
      let errorCode = error.code;
      let errorMessage = error.message;
      console.log("Error : " + errorCode + "-" + errorMessage);
      self.vue.message = errorCode + "-" + errorMessage;
      self.vue.is_messagebox_show = true;
    });
  };

  self.login = function() {
    var userEmail = document.getElementById("username_field").value;
    var userPass = document.getElementById("password_field").value;

    console.log(userEmail + " " + userPass);
    firebase.auth().signInWithEmailAndPassword(userEmail, userPass).catch(function(error) {
      // Handle Errors here.
      let errorCode = error.code;
      let errorMessage = error.message;
      console.log("Error : " + errorCode + "-" + errorMessage);
      self.vue.message = errorCode + "-" + errorMessage;
      self.vue.is_messagebox_show = true;
    });
  };

  self.signup = function() {
    var userEmail = document.getElementById("username_signup_field").value;
    var userPwd1 = document.getElementById("password_signup_field").value;
    var userPwd2 = document.getElementById("re-password_signup_field").value;

    if (!(userEmail && userPwd1 && userPwd2)) {
      self.vue.login_message = "The Email and Password must be filled";
      self.vue.is_login_messagebox_show = true;
      return;
    }
    if (userPwd1 != userPwd2) {
      self.vue.login_message = "The passwords you entered are not the same";
      self.vue.is_login_messagebox_show = true;
      return;
    }

    firebase.auth().createUserWithEmailAndPassword(userEmail, userPwd1).catch(function(error) {
      // Handle Errors here.
      var errorCode = error.code;
      var errorMessage = error.message;
      console.log("An error happened when handling signup");
      console.log("errorCode = ", errorCode, " errorMessage = ", errorMessage);
      self.vue.login_message = errorMessage;
      self.vue.is_login_messagebox_show = true;

      // ...

    }).then(function() {
      var user = firebase.auth().currentUser;
      if (user) {
        console.log("In signup: detected a user");
        var db = firebase.firestore();
        var user_uid = user.uid;
        db.collection("users").doc(user_uid).set({
          email: user.email,
          gender: '',
          major: '',
          name: '',
          university: '',
          ps: ''
        });
        user.sendEmailVerification().then(function() {
          // Email sent.
          console.log("A email is sent to the user");
          self.vue.login_message = "A email is sent to the addres you registed, please verify.";
          self.vue.is_login_messagebox_show = true;
        }).catch(function(error) {
          // An error happened.
          var errorCode = error.code;
          var errorMessage = error.message;
          console.log("An error happened when handling signup");
          console.log("errorCode = ", errorCode, " errorMessage = ", errorMessage);
          self.vue.login_message = errorMessage;
          self.vue.is_login_messagebox_show = true;
        });
      } else {
        console.log("In signup: cannot detect a user");
      }
    });
  }

  self.updateProfile = function() {
    var db = firebase.firestore();
    var user = firebase.auth().currentUser;
    var user_uid = user.uid;
    db.collection("users").doc(user_uid).set({
        email: user.email,
        gender: self.vue.profile_gender.toLowerCase(),
        major: self.vue.profile_major,
        name: self.vue.profile_name,
        university: /\(([^)]+)\)/.exec(self.vue.profile_university)[1].toLowerCase(),
        ps: self.vue.profile_personal_statement
      })
      .then(function() {
        console.log("Document successfully written!");
        self.vue.main_idx = "HOME";
      })
      .catch(function(error) {
        console.error("Error writing document: ", error);
        var errorCode = error.code;
        var errorMessage = error.message;
        console.log("An error happened when handling signup");
        console.log("errorCode = ", errorCode, " errorMessage = ", errorMessage);
        self.vue.login_message = errorMessage;
        self.vue.is_login_messagebox_show = true;
      });
  }

  self.updateTutorProfile = function() {
    var db = firebase.firestore();
    var user = firebase.auth().currentUser;
    var user_uid = user.uid;
    /* tutorCard format:
    var tutorCard = {
      data: {
        school: this.profile_university,
        course: '',
        grade: ''
      },
      index: index,
      is_active: true
    };*/
    for (index in self.vue.tutor_card_list) {
      var tutorCard = self.vue.tutor_card_list[index];
      if ((!tutorCard.is_active) && tutorCard.data.school && tutorCard.data.course) {
        var schoolName = /\(([^)]+)\)/.exec(tutorCard.data.school)[1].toLowerCase();
        var courseName = tutorCard.data.course.replace(/[^A-Za-z0-9]+/g, '').toLowerCase();
        var courseKey = schoolName + "-" + courseName;
        db.collection("users").doc(user_uid).collection("courses").doc(courseKey).delete()
        db.collection("schools").doc(schoolName).collection("courses").doc(courseName).collection("tutors").doc(user_uid).delete();
      }
    }
    for (index in self.vue.tutor_card_list) {
      var tutorCard = self.vue.tutor_card_list[index];
      if (tutorCard.is_active && tutorCard.data.school && tutorCard.data.course && tutorCard.data.grade) {
        var schoolName = /\(([^)]+)\)/.exec(tutorCard.data.school)[1].toLowerCase();
        var courseName = tutorCard.data.course.replace(/[^A-Za-z0-9]+/g, '').toLowerCase();
        var grade = tutorCard.data.grade.toUpperCase();
        var courseKey = schoolName + "-" + courseName;
        db.collection("users").doc(user_uid).collection("courses").doc(courseKey).set({
          school: schoolName,
          course: courseName,
          grade: grade
        })
        db.collection("schools").doc(schoolName).collection("courses").doc(courseName).set({});
        db.collection("schools").doc(schoolName).collection("courses").doc(courseName).collection("tutors").doc(user_uid).set({
          school: schoolName,
          course: courseName,
          grade: grade
        });
      }
    }
    //self.vue.main_idx = "HOME";

  }

  /*********************************************************************************************************/
  /*Signup functions*/



  self.vue = new Vue({
    el: "#vue-index",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
      // login-part
      logged_in: false,
      login_idx: "LOGIN",

      // login-part message box
      is_login_messagebox_show: false,
      login_message: "",

      // main-part
      main_idx: "HOME",

      // self profile
      profile_email: '',
      profile_name: '',
      profile_university: '',
      profile_gender: '',
      profile_major: '',
      profile_personal_statement: '',
      become_a_TA: false,
      profile_major_list: [],

      tutor_card_list: [],

      school_name_dict: {
        bc: 'Boston College (BC)',
        ucb: 'University of California, Berkeley (UCB)',
        ucsd: 'University of California, San Diego (UCSD)',
        ucla: 'University of California, Los Angeles (UCLA)',
        ucsb: 'University of California, Santa Barbara (UCSB)',
        ucsf: 'University of California, San Francisco (UCSF)',
        uci: 'University of California, Irvine (UCI)',
        ucr: 'University of California, Riverside (UCR)',
        ucsc: 'University of California, Santa Cruz (UCSC)',
        urm: 'University of California, Merced (UCM)',
        ucd: 'University of California, Davis (UCD)',
        uic: 'University of Illinois at Chicago (UIC)',
        ubc: 'University of British Columbia (UBC)'
      },

      school_list: ['Boston College (BC)',
        'University of California, Berkeley (UCB)',
        'University of California, San Diego (UCSD)',
        'University of California, Los Angeles (UCLA)',
        'University of California, Santa Barbara (UCSB)',
        'University of California, San Francisco (UCSF)',
        'University of California, Irvine (UCI)',
        'University of California, Riverside (UCR)',
        'University of California, Santa Cruz (UCSC)',
        'University of California, Merced (UCM)',
        'University of California, Davis (UCD)',
        'University of Illinois at Chicago (UIC)',
        'University of British Columbia (UBC)'
      ],

      school_data: {}
      //signup part
      // form_title: "",
      // form_content: "",
      // post_list: [],
      // star_indices: [1, 2, 3, 4, 5],
    },
    methods: {
      // login-part
      is_logged_in: self.is_logged_in,
      login: self.login,
      logout: self.logout,
      signup: self.signup,
      updateProfile: self.updateProfile,

      newTutorCard: function() {
        console.log("a mew ta card is created");
        var index = this.tutor_card_list.length;
        var tutorCard = {
          data: {
            school: this.profile_university,
            course: '',
            grade: ''
          },
          index: index,
          is_active: true
        };
        this.tutor_card_list.push(tutorCard);
      },
      updateTutorProfile: self.updateTutorProfile,

      // add_post: self.add_post,
      // // Likers.
      // like_mouseover: self.like_mouseover,
      // like_mouseout: self.like_mouseout,
      // like_click: self.like_click,
      // // Show/hide who liked.
      // show_likers: self.show_likers,
      // hide_likers: self.hide_likers,
      // // Star ratings.
      // stars_out: self.stars_out,
      // stars_over: self.stars_over,
      // set_stars: self.set_stars
    },
    watch: {
      profile_university: function(newSchool, oldSchool) {
        var schoolAbbr = /\(([^)]+)\)/.exec(newSchool)[1].toLowerCase();
        if (!(schoolAbbr in this.school_data)) {
          var db = firebase.firestore();
          var schoolRef = db.collection("schools").doc(schoolAbbr);
          var that = this;
          schoolRef.get().then(function(doc){
            if(doc.exists) {
              that.school_data[schoolAbbr] = doc.data();
              that.profile_major_list = that.school_data[schoolAbbr].major_list;
            }
          });
        } else {
          this.profile_major_list = this.school_data[schoolAbbr].major_list;
        }
      }
    },

  });

  // If we are logged in, shows the form to add posts.
  //self.is_logged_in();
  self.is_logged_in_listener();

  // Gets the posts.
  // self.get_posts();

  return self;
};




var APP = null;

// No, this would evaluate it too soon.
// var APP = app();

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function() {
  APP = app();
});
