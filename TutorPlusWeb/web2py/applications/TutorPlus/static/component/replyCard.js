var Template = `
<div class="reply-div" style="margin-top:100px">
  <v-container fluid grid-list-md>
    <v-layout align-space-between column>
      <v-layout row>

      <v-flex xs3>
        <v-rating v-model="show_rating" hover readonly></v-rating>
      </v-flex>

      <v-flex xs2>
        <v-btn flat color="primary" v-show="is_author">Edit</v-btn>
      </v-flex>
      <v-flex xs2>
        <v-btn flat color="primary" v-show="is_author">Delete</v-btn>
      </v-flex>
      <v-flex xs2>
        <v-btn flat color="primary" v-show="is_author">Submit</v-btn>
      </v-flex>

      <v-flex xs2>
          <v-layout row>
            <v-flex xs3>
              <v-btn fab dark small color="primary">
                <v-icon dark v-on:click="moveLeft()">chevron_left</v-icon>
              </v-btn>
            </v-flex>

            <v-flex xs3>
              <v-btn fab dark small color="primary">
                <v-icon dark v-on:click="moveRight()">chevron_right</v-icon>
              </v-btn>
            </v-flex>

            <v-flex xs2>
              <span>[{{index+1}}/{{index_max-1}}]</span>
            </v-flex>
            </v-layout>
        </v-flex>

        </v-layout>
      <v-textarea class="replies" v-model="show_reply" name="input-7-1" box label="Label" auto-grow readonly background-color="white"></v-textarea>
    </v-layout>
  </v-container>
</div>
`;

Vue.component('reply-card', {
  props: [
    'reply_list',
    'user_uid'
  ],
  data: function() {
    return {
      index: 0,
      index_max: 0,
      show_index: 0,
      show_reply: "",
      show_rating: 0,
      show_name: "",
      is_author: false,
    }
  },
  methods: {
    showDetail: function() {
      //this.card.is_active = false;
      //this.tutor_card.is_active = false;
      this.$emit('show-detail', this.uid);
    },
    moveLeft: function() {
      if (this.index==0){
        this.index = this.index_max-1;
      } else {
        this.index = this.index - 1;
      }
      this.show_reply = this.reply_list[this.index].reply;
      this.show_rating = this.reply_list[this.index].rating;
      this.show_name = this.reply_list[this.index].name;
      if (this.reply_list[this.index].id == this.user_uid ){
        this.is_author = true;
      } else {
        this.is_author = false;
      }
    },
    moveRight: function() {
      if (this.index==this.index_max-1){
        this.index = 0;
      } else {
        this.index = this.index + 1;
      }
      this.show_reply = this.reply_list[this.index].reply;
      this.show_rating = this.reply_list[this.index].rating;
      this.show_name = this.reply_list[this.index].name;
      if (this.reply_list[this.index].id == this.user_uid ){
        this.is_author = true;
      } else {
        this.is_author = false;
      }
    }
  },
  created(){
    console.log(this.reply_list);
    this.index_max = this.reply_list.length;
    if (this.reply_list.length > 0) {
      this.show_reply = this.reply_list[0].reply;
      this.show_rating = this.reply_list[0].rating;
      this.show_name = this.reply_list[0].name;
    }
  },
  computed: {},
  template: Template
});
