var UserAuthenticationStatusView = Backbone.View.extend({
    template: _.template($('#tpl-user-authentication-status').html()),

    initialize: function() {
    },

    render: function() {
        this.$el.html(this.template());
    }
});