// This is the js for the default/index.html view.
    // register modal component
Vue.component('modal', {
  template: '#modal-template'
});

Vue.component('v-select', VueSelect.VueSelect);


var Template_TA_Course_Card = `
<div v-if="card.is_active" style="padding:10px; margin-bottom:30px; border-radius: 3px; box-shadow: 0px 2px 2px 0px rgba(0, 0, 0, 0.15); border: 1px solid #e0e0e0;">
  <v-select v-model="card.data.school" :options="['Boston College (BC)',
                  'University of California, Santa Cruz (UCSC)',
                  'University of California, San Francisco (UCSF)',
                  'University of California, Davis (UCD)',
                  'University of Illinois at Chicago (UIC)',
                  'University of British Columbia (UBC)'
                  ]"
    placeholder="School"></v-select>
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

Vue.component('ta-course-card',{
  props:[
    'card'
  ],
  data: function () {
    return {
      grade:'',
      course:'',
      school:''
    }
  },
  methods: {
    deleteThis: function() {
      this.card.is_active = false;
      //this.tutor_card.is_active = false;
      //this.$emit(this.tutor_card.index);
    }
  },
  computed: {
  },
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
    var enumerate = function(v) { var k=0; return v.map(function(e) {e._idx = k++;});};



    /*********************************************************************************************************/
    /*Login functions*/
    self.is_logged_in_listener = function(){
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
                if (user.emailVerified == true){
                  console.log("At user listener: your email has been verified");
                  console.log("The uid of the user is:", user.uid);
                  self.vue.logged_in = true;
                } else {
                  console.log("At user listener: your email is not verified yet");
                  self.vue.logged_in = false;
                }
            } else{
              // not logging in
                self.vue.logged_in = false;
                console.log("User listener: logout!");
            }
        });
    };

    self.is_logged_in = function(){
        let user = firebase.auth().currentUser;
        var login_state = false;

        if (user) {
          login_state = true;
        }

        self.vue.logged_in = login_state;
    };

    self.logout = function(){
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

    self.login = function(){
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

    self.signup = function () {
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

      }).then(function(){
        var user = firebase.auth().currentUser;
        if (user) {
          console.log("In signup: detected a user");
          user.sendEmailVerification().then(function() {
              // Email sent.
              console.log("A email is sent to the user");
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

    self.updateProfile = function (){
      var db = firebase.firestore();
      var user = firebase.auth().currentUser;
      var user_uid = user.uid;
      db.collection("users").doc(user_uid).set({
          email: user.email,
          gender: self.vue.profile_gender.toLowerCase(),
          major: self.vue.profile_major,
          name: self.vue.profile_name,
          university: /\(([^)]+)\)/.exec(self.vue.profile_university)[1].toLowerCase()
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
            login_message:"",

            // main-part
            main_idx: "HOME",

            // self profile
            profile_name: '',
            profile_university: '',
            profile_gender: '',
            profile_major: '',
            become_a_TA: false,

            tutor_card_list: [],

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
            deleteTutorCard: function(index) {
              delete this.tutor_card_list.index;
            },
            updateTutoeCard: function() {
              for (index in tutor_card_list) {
                if (tutor_card_list[index].is_active) {
                  
                }
              }
            }
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
        computed: {
        }

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
jQuery(function(){APP = app();});
