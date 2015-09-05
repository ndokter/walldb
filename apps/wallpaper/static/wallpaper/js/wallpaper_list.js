function WallpaperList(el, resource_url, options) {
    this.el = el;
    this.is_loading = false;
    this.next_page_url = resource_url;
    this.options = typeof options !== 'undefined' ? options : {};

    this.random_ordering_seed = null;

    this.initialize();
}

WallpaperList.prototype.load = function(success_callback) {
    var self = this,
        wallpaper_template = _.template($('#wallpaper-thumbnail-template').html()),
        url = this.next_page_url,
        query_parameters = $.getQueryParameters();

    // The seed is needed when ordering randomly.
    if (self.random_ordering_seed === null) {
        self.random_ordering_seed = (Math.random()).toFixed(8);
    }

    query_parameters.seed = self.random_ordering_seed;

    // TODO reduce the amount of code for GET parameter copying and cleaning.
    if (self.options.copy_url_parameters && query_parameters.resolution) {
        // Quickfix to translate the resolution parameter to a width and height.
        var resolution_parts = query_parameters.resolution.split('x');

        query_parameters.width = resolution_parts[0];
        query_parameters.height = resolution_parts[1];

        delete query_parameters.resolution;
    }

    var parsed_url = URI.parse(url);

    if (parsed_url.query) {
        var parsed_query = URI.parseQuery(parsed_url.query);

        query_parameters = $.extend({}, query_parameters, parsed_query);
    }

    url = URI(url).query(query_parameters);

    $.get(url, null, function(response) {
        self.next_page_url = response.next;

        // Render all thumbnails and then add them in 1 go. This makes the page
        // less jumpy.
        var thumbnails = [];

        $.each(response.results, function(index, result) {
            thumbnails.push($('<li/>').append(
                new Thumbnail(result, wallpaper_template).render())
            );
        });

        self.el.append(thumbnails);

        self.is_loading = false;

        // Small hack to make sure that the screen gets loaded to the bottom. The user
        // can scroll further from there on.
        $(self).trigger('scroll');
    });
};

WallpaperList.prototype.initialize = function() {
    var self = this;

    // Initial.
    this.load();

    // Endless scrolling.
    $(window).scroll(function() {
        if ($(window).scrollTop() + 400 >= ($(document).height() - ($(window).height()))) {
            // Prevent multiple simultaneous requests when scrolling near the bottom, while wallpapers are
            // being fetched. Also stop sending requests when no more wallpapers can be found.
            if (!self.is_loading && self.next_page_url && !self.options.no_scroll) {
                self.is_loading = true;

                self.load();
            }
        }
    });
}