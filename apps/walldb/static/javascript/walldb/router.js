var WallDB = Backbone.Router.extend({
    routes: {
        '': 'wallpaperIndex',
        'login': 'userAuthentication',
        'register': 'userAuthentication'
    },

    initialize: function() {
        if (!this.applicationMainView) {
            this.applicationMainView = new ApplicationMainView({el: 'body'});
        }

        this.applicationMainView.render();
    },

    wallpaperIndex: function() {
        this.applicationMainView.renderWallpaperIndex();
    },

    'userAuthentication': function() {
        this.applicationMainView.renderUserAuthenticationLogin();
    }
});