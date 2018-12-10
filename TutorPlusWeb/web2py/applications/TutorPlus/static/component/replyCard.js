var Template = `
<div class="reply-div" style="margin-top:100px">
  <v-container fluid grid-list-md v-if="!is_editing">
    <v-layout align-space-between column>

      <v-layout row>

      <v-flex xs3>
        <v-rating v-model="show_rating" hover readonly></v-rating>
      </v-flex>

      <v-flex xs2>
        <v-btn flat color="primary" v-show="false">Edit</v-btn>
      </v-flex>
      <v-flex xs2>
        <v-btn flat color="primary" v-show="false">Delete</v-btn>
      </v-flex>
      <v-flex xs2>
        <v-btn flat color="primary" v-show="false">Submit</v-btn>
      </v-flex>

        <v-flex xs2>
          <v-layout row>
            <v-flex xs3>
              <v-btn fab dark small color="primary" v-on:click="moveLeft()">
                <v-icon dark >chevron_left</v-icon>
              </v-btn>
            </v-flex>

            <v-flex xs3>
              <v-btn fab dark small color="primary" v-on:click="moveRight()">
                <v-icon dark >chevron_right</v-icon>
              </v-btn>
            </v-flex>

            <v-flex xs2>
              <span>[{{index+1}}/{{index_max+1}}]</span>
            </v-flex>

            <v-flex xs2>
              <v-btn flat color="blue" v-on:click="is_editing=true">New Reply</v-btn>
            </v-flex>

          </v-layout>
        </v-flex>

        </v-layout>

      <v-textarea class="replies" v-model="show_reply" name="input-7-1" box label="Label" auto-grow readonly background-color="white"></v-textarea>
    </v-layout>
  </v-container>


  <v-container fluid grid-list-md v-if="is_editing">
    <v-layout align-space-between column>

      <v-layout row>

  <v-flex xs3>
    <v-rating v-model="reply_rating" hover></v-rating>
  </v-flex>

  <v-flex xs2>
    <v-btn flat color="primary" v-show="false">Edit</v-btn>
  </v-flex>
  <v-flex xs2>
    <v-btn flat color="primary" v-show="false">Delete</v-btn>
  </v-flex>
  <v-flex xs2>
    <v-btn flat color="primary" v-show="false">Submit</v-btn>
  </v-flex>

    <v-flex xs2>
      <v-layout row>

        <v-flex xs2>
          <v-btn flat color="blue" v-on:click="is_editing=false">Return</v-btn>
        </v-flex>

        <v-flex xs4>
          <v-btn fab dark small color="primary" v-show="false" v-on:click="moveLeft()">
            <v-icon dark >chevron_left</v-icon>
          </v-btn>
        </v-flex>

        <v-flex xs2 style="margin-left:10px">
          <v-btn flat color="blue" v-on:click="submitReply()">Submit</v-btn>
        </v-flex>

      </v-layout>
    </v-flex>

    </v-layout>

    <v-textarea class="replies" v-model="reply_reply" name="input-7-1" box label="Label" auto-grow background-color="white"></v-textarea>
  </v-layout>
</v-container>


</div>
`;

Vue.component('reply-card', {
  props: [
    'reply_list',
    'user_uid',
    'id_token',
    'tutor_uid',
    'user_name'
  ],
  data: function() {
    return {
      index: 0,
      index_max: 0,
      show_index: 0,
      show_reply: "",
      show_rating: 0,
      show_name: "",

      reply_rating: 0,
      reply_reply: "",

      is_author: false,
      is_editing: false,
    }
  },
  methods: {
    showDetail: function() {
      //this.card.is_active = false;
      //this.tutor_card.is_active = false;
      this.$emit('show-detail', this.uid);
    },
    moveLeft: function() {
      if (this.index == 0) {
        this.index = this.index_max;
      } else {
        this.index = this.index - 1;
      }
      this.show_reply = this.reply_list[this.index].reply;
      this.show_rating = Number(this.reply_list[this.index].rating);
      this.show_name = this.reply_list[this.index].name;
      if (this.reply_list[this.index].id == this.user_uid) {
        this.is_author = true;
      } else {
        this.is_author = false;
      }
    },
    moveRight: function() {
      if (this.index == this.index_max) {
        this.index = 0;
      } else {
        this.index = this.index + 1;
      }
      this.show_reply = this.reply_list[this.index].reply;
      this.show_rating = Number(this.reply_list[this.index].rating);
      this.show_name = this.reply_list[this.index].name;
      if (this.reply_list[this.index].id == this.user_uid) {
        this.is_author = true;
      } else {
        this.is_author = false;
      }
    },
    submitReply:function() {
      var packet = {
        idToken: this.id_token,
        data: {
          id: this.user_uid,
          tutor_id: this.tutor_uid,
          name: this.user_name,
          rating: this.reply_rating,
          reply: this.reply_reply
        }
      }
      console.log(packet);
      $.get("https://tutorplus-93a0f.appspot.com/upload-user-rating", packet,
        function(data, status) {
          console.log("hello wolrd in query2");
          console.log(data);
          console.log(data.profile)
        });

    }
  },
  watch: {
    reply_list: function() {
      //console.log("In reply card");
      //console.log(this.reply_list.length);
      this.index_max = this.reply_list.length - 1;
      if (this.reply_list.length > 0) {
        this.show_reply = this.reply_list[0].reply;
        this.show_rating = Number(this.reply_list[0].rating);
        this.show_name = this.reply_list[0].name;
      }
    }
  },
  created() {

  },
  computed: {},
  template: Template
});
