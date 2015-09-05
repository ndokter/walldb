var ApplicationMainView = Backbone.View.extend({
    template: _.template($('#tpl-main').html()),

    initialize: function() {
    },

    render: function() {
        this.$el.html(this.template());

        this.renderHeader();
    },

    renderHeader: function() {
        if (!this.applicationHeaderView) {
            this.applicationHeaderView = new ApplicationHeaderView({el: 'header'});
        }

        this.applicationHeaderView.render()
    },

    renderWallpaperIndex: function() {
        if (!this.wallpaperIndexView) {
            this.wallpaperIndexView = new WallpapersIndexView({el: '#main'});
        }

        this.wallpaperIndexView.render()
    },

    renderUserAuthenticationLogin: function() {
        if (!this.userAuthenticationView) {
            this.userAuthenticationView = new UserAuthenticationView({el: '#main'});
        }

        this.userAuthenticationView.render();
    }
});