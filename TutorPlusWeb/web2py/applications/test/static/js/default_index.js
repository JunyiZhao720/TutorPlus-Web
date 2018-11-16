// This is the js for the default/index.html view.
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

    self.add_post = function () {
        // We disable the button, to prevent double submission.
        $.web2py.disableElement($("#add-post"));
        var sent_title = self.vue.form_title; // Makes a copy 
        var sent_content = self.vue.form_content; // 
        $.post(add_post_url,
            // Data we are sending.
            {
                post_title: self.vue.form_title,
                post_content: self.vue.form_content
            },
            // What do we do when the post succeeds?
            function (data) {
                // Re-enable the button.
                $.web2py.enableElement($("#add-post"));
                // Clears the form.
                self.vue.form_title = "";
                self.vue.form_content = "";
                // Adds the post to the list of posts. 
                var new_post = {
                    id: data.post_id,
                    post_title: sent_title,
                    post_content: sent_content,
                    thumb_count: 0
                };
                self.vue.post_list.unshift(new_post);
                // We re-enumerate the array.
                self.process_posts();
            });
        // If you put code here, it is run BEFORE the call comes back.
    };

    self.get_posts = function() {
        $.getJSON(get_post_list_url,
            function(data) {
                // I am assuming here that the server gives me a nice list
                // of posts, all ready for display.
                self.vue.post_list = data.post_list;
                // Post-processing.
                self.process_posts();
                console.log("I got my list");
            }
        );
        console.log("I fired the get");
    };

    self.process_posts = function() {
        // This function is used to post-process posts, after the list has been modified
        // or after we have gotten new posts. 
        // We add the _idx attribute to the posts. 
        enumerate(self.vue.post_list);
        // We initialize the smile status to match the like. 
        self.vue.post_list.map(function (e) {
            // I need to use Vue.set here, because I am adding a new watched attribute
            // to an object.  See https://vuejs.org/v2/guide/list.html#Object-Change-Detection-Caveats
            // The code below is commented out, as we don't have smiles any more. 
            // Replace it with the appropriate code for thumbs. 
            // // Did I like it? 
            // // If I do e._smile = e.like, then Vue won't see the changes to e._smile . 
            // Vue.set(e, '_smile', e.like); 
            Vue.set(e, '_tstatus', e.thumb);
            Vue.set(e, 'thumb_count', parseInt(e.thumb_count));
            Vue.set(e, '_color', 'black');
        });
    };

    self.thumb_mouseover_u = function (post_idx) {
        // When we mouse over something, the face has to assume the opposite
        // of the current state, to indicate the effect.
        var p = self.vue.post_list[post_idx];
        //var d = document.getElementById("tb")
        p._tstatus ='u'
        if(p._tstatus != p.thumb)
            p._color = 'grey';
            //d.style.color = "grey";
        
        else
            p._color = 'black';
            //d.style.color = "";

    };

    self.thumb_mouseover_d = function (post_idx) {
        // When we mouse over something, the face has to assume the opposite
        // of the current state, to indicate the effect.
        var p = self.vue.post_list[post_idx];
        //var d = document.getElementById("tb")
        p._tstatus ='d'
        if(p._tstatus != p.thumb)
            p._color = 'grey';
            //d.style.color = "grey";
        
        else
            p._color = 'black';
            //d.style.color = "";
    };

    self.thumb_click_u = function (post_idx) {
        // The like status is toggled; the UI is not changed.
        var p = self.vue.post_list[post_idx];
        //var index = 0;
        if (p.thumb == 'u'){
            p.thumb = null;
            p.thumb_count = parseInt(parseInt(p.thumb_count) - parseInt(1));
            //index = -1;
        }
        
        else if (p.thumb == 'd'){
            p.thumb = 'u'
            p.thumb_count = parseInt(parseInt(p.thumb_count) + parseInt(2));
            //index = 2;
        }
        else{
            p.thumb = 'u'
            p.thumb_count = parseInt(parseInt(p.thumb_count) + parseInt(1));
            //index = 1;
        }
        // We need to post back the change to the server.
        $.post(set_thumb_url, {
            post_id: p.id,
            thumb: p.thumb
        });
        $.post(update_count_url, {
            post_id: p.id,
            thumb_count: parseInt(p.thumb_count),
            //amount: parseInt(index),

        }); // Nothing to do upon completion.
    };
    
    self.thumb_click_d = function (post_idx) {
        // The like status is toggled; the UI is not changed.
        var p = self.vue.post_list[post_idx];
        if (p.thumb == 'd'){
            p.thumb = null;
            p.thumb_count = parseInt(parseInt(p.thumb_count) + parseInt(1));
            //index = 1;
        }
        
        else if (p.thumb == 'u'){
            p.thumb = 'd'
            p.thumb_count = parseInt(parseInt(p.thumb_count) - parseInt(2));
            //index = -2;
        }
        else{
            p.thumb = 'd'
            p.thumb_count = parseInt(parseInt(p.thumb_count) - parseInt(1));
            //index = -1;
        }
        // We need to post back the change to the server.
        $.post(set_thumb_url, {
            post_id: p.id,
            thumb: p.thumb
        }); 
        $.post(update_count_url, {
            post_id: p.id,
            thumb_count: parseInt(p.thumb_count),
            //amount: parseInt(index),
        });// Nothing to do upon completion.
    };

    self.thumb_mouseout = function (post_idx) {
        // The like and smile status coincide again.
        var p = self.vue.post_list[post_idx];
        //var d = document.getElementById("tb")
        //if (p.thumb =='u' || p.thumb == 'd')
        p._tstatus = p.thumb;
        //else
            //p._tstatus = null;
        //d.style.color="";
        p._color = 'black';
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            form_title: "",
            form_content: "",
            post_list: [],
            show_form: false,
        },
        methods: {
            add_post: self.add_post,

            thumb_mouseover_u: self.thumb_mouseover_u,
            thumb_mouseover_d: self.thumb_mouseover_d,
            thumb_mouseout: self.thumb_mouseout,
            thumb_click_u: self.thumb_click_u,
            thumb_click_d: self.thumb_click_d,
            toggle_form: function () {
                console.log("show_form was: " + this.show_form );
                this.show_form = !this.show_form
                console.log("show_form is now: " + this.show_form);
            }
        }

    });

    // If we are logged in, shows the form to add posts.
    if (is_logged_in) {
        $("#add_post").show();
    }

    // Gets the posts.
    self.get_posts();

    return self;
};

var APP = null;

// No, this would evaluate it too soon.
// var APP = app();

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
