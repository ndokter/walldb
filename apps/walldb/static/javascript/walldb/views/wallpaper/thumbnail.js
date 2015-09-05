var WallpaperIndexListWallpaperThumbnailView = Backbone.View.extend({
    tagName: 'li',
    className: 'thumbnail',
    template: _.template($('#tpl-wallpaper-thumbnail').html()),

    initialize: function() {
        this.render();
    },

    events: {
        'mouseover':'showOptions',
        'mouseout': 'hideOptions'
    },

    showOptions: function(e) {
        $('.options', e.currentTarget).show();
    },

    hideOptions: function(e) {
        $('.options', e.currentTarget).hide();
    },

    render: function() {
        this.$el.html(this.template({'model': this.model}));
    }
});