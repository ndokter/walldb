var UserAuthenticationView = Backbone.View.extend({
    template: _.template($('#tpl-user-authentication').html()),

    initialize: function() {
    },

    render: function() {
        this.$el.html(this.template());
    }
});