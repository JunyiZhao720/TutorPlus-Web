// This is the js for the default/index.html view.
// register modal component
Vue.component('modal', {
  template: '#modal-template'
});

//Vue.component('v-select', VueSelect.VueSelect);


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

        //firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
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

          firebase.auth().currentUser.getIdToken(true).then(function(idToken) {
            self.vue.idToken = idToken;
            console.log(idToken);
          });

          self.vue.user_uid = user.uid;
          self.vue.profile_email = user.email;

          var db = firebase.firestore();
          var user_uid = user.uid;
          var userRef = db.collection("users").doc(user_uid);
          userRef.get().then(function(doc) {
            if (doc.exists) {
              user_profile = doc.data();
              console.log("User document found");
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
        //var db = firebase.firestore();
        var user_uid = user.uid;
        /*
        db.collection("users").doc(user_uid).set({
          email: user.email,
          gender: '',
          major: '',
          name: '',
          university: '',
          ps: ''
        });*/
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
    var profile_university = '';
    if (self.vue.profile_university) {
      profile_university = /\(([^)]+)\)/.exec(self.vue.profile_university)[1].toLowerCase();
    }
    $.get("https://tutorplus-93a0f.appspot.com/update-profile",
    {
      idToken: self.vue.idToken,
      data: {
        id: self.vue.user_uid,
        //email: self.vue.profile_email,
        university: profile_university,
        gender: self.vue.profile_gender.toLowerCase(),
        major: self.vue.profile_major,
        name: self.vue.profile_name,
        ps: self.vue.profile_personal_statement
      }
    },
    function(data, status) {
      console.log(data);
    });
  }

  self.updateTutorProfile = function() {
    var packet = {
      idToken: self.vue.idToken,
      data: {
        id: self.vue.user_uid,
        courses: self.vue.tutor_card_list,
      }
    };
    var strPacket = JSON.stringify(packet);
    $.get("https://tutorplus-93a0f.appspot.com/upload-course-list-for-the-user", {packet: strPacket},
    function(data, status){
      console.log(data);
    });
  }

  self.searchTutorByCourse = function() {
    //console.log("hello")
    if (self.vue.search_course && self.vue.search_university) {
      var packet = {
        idToken: self.vue.idToken,
        data: {
          id: self.vue.user_uid,
          course_id: self.vue.search_course.split(" - ")[0].replace(/[\s]+/g, '').toLowerCase(),
          school_id: /\(([^)]+)\)/.exec(self.vue.search_university)[1].toLowerCase(),
        }
      };
      $.get("https://tutorplus-93a0f.appspot.com/download-tutor-profile-list", packet,
      function(data, status){
        //console.log("hello wolrd in GUHU")
        //console.log(data.profile_list);
        self.vue.search_result = data.profile_list;
        self.vue.search_show_grade = true;
      });
    }
  }

  self.searchTutorByName = function() {
    //console.log("hello in search by name");
    if (self.vue.search_name) {
      var packet = {
        idToken: self.vue.idToken,
        data: {
          name: self.vue.search_name,
        }
      };
      $.get("https://tutorplus-93a0f.appspot.com/download-tutor-profile-list-by-name", packet,
      function(data, status){
        //console.log("hello wolrd in GUHU");
        //console.log(data.profile_list);
        self.vue.search_result = data.profile_list;
        self.vue.search_show_grade = false;
      });
    }
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
      idToken: '',
      user_uid: '',
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

      search_university: '',
      search_course: '',
      search_name: '',
      search_course_list: [],
      search_result: [],
      search_show_grade: true,

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

      school_full_name_dict: {
        bc: 'Boston College',
        ucb: 'University of California, Berkeley',
        ucsd: 'University of California, San Diego',
        ucla: 'University of California, Los Angeles',
        ucsb: 'University of California, Santa Barbara',
        ucsf: 'University of California, San Francisco',
        uci: 'University of California, Irvine',
        ucr: 'University of California, Riverside',
        ucsc: 'University of California, Santa Cruz',
        urm: 'University of California, Merced',
        ucd: 'University of California, Davis',
        uic: 'University of Illinois at Chicago',
        ubc: 'University of British Columbia'
      },


      school_list: [
        'University of California, Berkeley (UCB)',
        'University of California, San Diego (UCSD)',
        'University of California, Los Angeles (UCLA)',
        'University of California, Irvine (UCI)',
        'University of California, Santa Cruz (UCSC)',
        'University of California, Davis (UCD)',
      ],

      school_data: {},

      detailPage: "BalaBla"
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
            school: '',
            course: '',
            grade: ''
          },
          index: index,
          is_active: true
        };
        if (this.profile_university) {
          tutorCard.data.school = /\(([^)]+)\)/.exec(this.profile_university)[1].toLowerCase();
        }
        this.tutor_card_list.push(tutorCard);
      },
      updateTutorProfile: self.updateTutorProfile,
      searchTutorByCourse: self.searchTutorByCourse,
      searchTutorByName: self.searchTutorByName,

      queryTest: function() {
        console.log("hello in query1");
        var packet = {
          idToken: self.vue.idToken,
          data: {
            id: "SAMPLE"
          }
        }
        console.log(packet);
        $.get("https://tutorplus-93a0f.appspot.com/get-profile", packet,
        function(data, status){
          console.log("hello wolrd in query2");
          console.log(data);
          console.log(data.profile)
        });
      },

      showTutorDetail: function(uid){
        this.detailPage= uid;
        this.main_idx = 'RESULT';
        var packet = {
          idToken: self.vue.idToken,
          data: {
            id: uid,
          }
        }
        //console.log(packet);
        console.log("before get")
        $.get("https://tutorplus-93a0f.appspot.com/get-profile", packet,
        function(data, status){
          console.log("after get")
          console.log(data.profile)
        });
      }

    },
    watch: {
      profile_university: function(newSchool, oldSchool) {
        if (!newSchool) {
          this.profile_major_list = [];
        } else {
          var schoolAbbr = /\(([^)]+)\)/.exec(newSchool)[1].toLowerCase();
          if (!(schoolAbbr in this.school_data)) {
            var that = this;
            this.$http.get("https://tutorplus-93a0f.appspot.com/download-school-fields", {params: {school_id: schoolAbbr}}).then(function (data){
              that.school_data[schoolAbbr] = data.body.school;
              course_list = data.body.school.course_list;
              that.profile_major_list = that.school_data[schoolAbbr].major_list;

              var course_name_dict = {};
              for (i = 0; i < course_list.length; i++) {
                var course_key = course_list[i].split(" - ")[0].replace(/[\s]+/g, '').toLowerCase();
                course_name_dict[course_key]= course_list[i];
              }
              that.school_data[schoolAbbr].course_name_dict = course_name_dict;
            });
          } else {
            this.profile_major_list = this.school_data[schoolAbbr].major_list;
          }
        }
      },
      search_university: function(newSchool, oldSchool) {
        if (!newSchool) {
          this.search_course_list = [];
        } else {
          var schoolAbbr = /\(([^)]+)\)/.exec(newSchool)[1].toLowerCase();
          if (!(schoolAbbr in this.school_data)) {
            var that = this;
            this.$http.get("https://tutorplus-93a0f.appspot.com/download-school-fields", {params: {school_id: schoolAbbr}}).then(function (data){
              that.school_data[schoolAbbr] = data.body.school;
              that.search_course_list = that.school_data[schoolAbbr].course_list;

              var course_name_dict = {};
              for (i = 0; i < course_list.length; i++) {
                var course_key = course_list[i].split(" - ")[0].replace(/[\s]+/g, '').toLowerCase();
                course_name_dict[course_key]= course_list[i];
              }
              that.school_data[schoolAbbr].course_name_dict = course_name_dict;
            });
          } else {
            this.search_course_list = this.school_data[schoolAbbr].course_list;
          }
        }
      },
      idToken: function(newStatus, oldStatus) {
        if (newStatus) {
          var that = this;
          this.$http.get("https://tutorplus-93a0f.appspot.com/get-profile",
          {
            params: {
              idToken: this.idToken,
              data:{id: this.user_uid}
            }
          })
          .then(function (data){
            user_profile = data.body.profile;
            if (user_profile.name) {
              that.profile_name = user_profile.name;
            } else {
              that.profile_name = '';
            }
            if (user_profile.university) {
              that.profile_university = that.school_name_dict[user_profile.university];
            } else {
              that.profile_university = '';
            }
            if (user_profile.gender) {
              that.profile_gender = (user_profile.gender.toLowerCase() == 'male') ? 'Male' : 'Female';
            } else {
              that.profile_gender = '';
            }
            if (user_profile.major) {
              that.profile_major = user_profile.major;
            } else {
              that.profile_major = '';
            }
            if(user_profile.ps) {
              that.profile_personal_statement = user_profile.ps;
            } else {
              that.profile_personal_statement = '';
            }
            //that.profile_email = user_profile.email;
          });
          this.tutor_card_list = [];
          this.$http.get("https://tutorplus-93a0f.appspot.com/download-course-list-for-the-user",
          {
            params: {
              idToken: this.idToken,
              data:{id: this.user_uid}
            }
          })
          .then(function (data){
            var tutorCourseList = data.body.course_list_user;
            var newList = []
            for (i = 0; i < tutorCourseList.length; i++) {
              var tutorCard = {
                data: {
                  school: tutorCourseList[i].school,
                  course: tutorCourseList[i].course,
                  grade: tutorCourseList[i].grade
                },
                index: i,
                is_active: true
              };
              newList.push(tutorCard);
            }
            that.tutor_card_list = newList;
          });
        } else {
          this.profile_name = '';
          this.profile_university = '';
          this.profile_gender = '';
          this.profile_major = '';
          this.profile_personal_statement = '';
          this.tutor_card_list = [];
        }
      },
      become_a_TA: function() {
        /*
        if (this.become_a_TA) {
          var that = this;
          this.$http.get("https://tutorplus-93a0f.appspot.com/download-course-list-for-the-user",
          {
            params: {
              idToken: this.idToken,
              data:{id: this.user_uid}
            }
          })
          .then(function (data){
            var tutorCourseList = data.body.course_list_user;
            var newList = []
            for (i = 0; i < tutorCourseList.length; i++) {
              var tutorCard = {
                data: {
                  school: tutorCourseList[i].school,
                  course: tutorCourseList[i].course,
                  grade: tutorCourseList[i].grade
                },
                index: i,
                is_active: true
              };
              newList.push(tutorCard);
            }
            that.tutor_card_list = newList;
          });
        }*/
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
