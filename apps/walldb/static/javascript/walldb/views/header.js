var ApplicationHeaderView = Backbone.View.extend({
    template: _.template($('#tpl-header').html()),

    initialize: function() {
    },

    render: function() {
        this.$el.html(this.template());

        this.renderAuthenticationStatus();
    },

    renderAuthenticationStatus: function() {
        if (!this.userAuthenticationStatusView) {
            this.userAuthenticationStatusView = new UserAuthenticationStatusView({el: '#login-status'});
        }

        this.userAuthenticationStatusView.render()
    }
});