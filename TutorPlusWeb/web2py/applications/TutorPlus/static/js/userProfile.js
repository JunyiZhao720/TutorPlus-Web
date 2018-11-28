var template: `
<div class="rs-select2 js-select-simple select2-search">
  <select name="profile_university" id="profile_university" value="">
    <option disabled="disabled" value="" selected>University</option>
    <option value="">Refuse to Claim</option>
    <option value="bc">Boston College (BC)</option>
    <option value="ucsf">University of California, San Francisco (UCSF)</option>
    <option value="ucsc">University of California, Santa Cruz (UCSC)</option>
    <option value="ucd">University of California, Davis (UCD)</option>
    <option value="uic">University of Illinois at Chicago (UIC)</option>
    <option value="ubc">University of British Columbia (UBC)</option>
  </select>
  <div class="select-dropdown"></div>
</div>`;

Vue.component('jqselecter', {
  template: template,
  props: [],
  mounted: function() {
    var self = this;
    $(this.$el).datepicker({
      dateFormat: this.dateFormat,
      onSelect: function(date) {
        self.$emit('update-date', date);
      }
    });
    },

    beforeDestroy: function() {
      $(this.$el).datepicker('hide').datepicker('destroy');
    }
});
/*
new Vue({
  el: '#university-selector',
  delimiters: ['${', '}'],
  data: {
    hello: "hello world";
  },
  methods: {
  }
});
*/
