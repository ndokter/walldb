var WallpaperModel = Backbone.Model.extend({});

var WallpapersCollection = Backbone.Collection.extend({
    model: WallpaperModel,
    url: '/wallpapers',
});