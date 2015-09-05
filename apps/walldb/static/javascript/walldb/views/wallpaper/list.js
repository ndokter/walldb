var WallpapersIndexListView = Backbone.View.extend({
    initialize: function() {
    },

    render: function(collection) {
        var that = this;

        this.$el.html('');

        collection.each(function(wallpaper) {
            that.$el.append(new WallpaperIndexListWallpaperThumbnailView({model: wallpaper.get('thumbnails')[0]}).el);
        });
    }
});