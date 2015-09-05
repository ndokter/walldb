var WallpapersIndexView = Backbone.View.extend({
    template: _.template($('#tpl-wallpaper-list').html()),

    initialize: function() {
        this.collection = new WallpapersCollection();
    },

    render: function () {
        this.$el.html(this.template());

        this.renderWallpaperList();
    },

    renderWallpaperList: function() {
        var that = this;

        if (!this.wallpaperIndexListView) {
            this.wallpaperIndexListView = new WallpapersIndexListView({el: 'ul'});
        }

        this.collection.fetch({
            success: function () {
                that.wallpaperIndexListView.render(that.collection);
            }
        });
    }
});