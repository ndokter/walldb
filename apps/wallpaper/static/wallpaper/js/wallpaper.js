var Wallpaper = function (data, template) {
    this.data = data;
    this.template = template;
    this.$el = null;
}

Wallpaper.prototype.rate = function(self, that, e) {
    e.preventDefault();

    var $thumbnail = self.$el.closest('div'),
        img_data = $('img', $thumbnail).data(),
        button_data = $(that).data()
        request_type = null;

    if (self.data.user_rating === null) {
        request_type = 'POST';
    } else if (self.data.user_rating !== button_data.scoreValue) {
        request_type = 'PUT';
    } else {
        request_type = 'DELETE';
    }

    $.ajax({
        url: '/api/v1/wallpaper/' + img_data.wallpaperId + '/rate/',
        type: request_type,
        data: {score: button_data.scoreValue},
        success: function(result) {
            var rating_button_els = $('.rating', $thumbnail);
            rating_button_els.removeClass('active');

            if (result === undefined) {
                // Delete has no result response.
                self.data.user_rating = null;
            } else {
                self.data.user_rating = result.score;
                $('.rating[data-score-value="' + result.score + '"]', $thumbnail).toggleClass('active');
            }
        },
        statusCode: {
            403: function() {
                $('#authentication-required').modal('show');
            }
        }
    });
};

Wallpaper.prototype.favorite = function(self, that, e) {
    e.preventDefault();

    var thumbnail_el = self.$el.closest('div'),
        img_data = $('img', thumbnail_el).data(),
        request_type = self.data.user_favorite ? 'DELETE' : 'POST';

    $.ajax({
        url: '/api/v1/wallpaper/' + img_data.wallpaperId + '/favorite/',
        type: request_type,
        success: function(result) {
            self.data.user_favorite = (result !== undefined);

            $(that).toggleClass('active', self.data.user_favorite);
        },
        statusCode: {
            403: function() {
                $('#authentication-required').modal('show');
            }
        }
    });
};

Wallpaper.prototype.render = function() {
    var self = this;
    this.$el = $(this.template({'wallpaper': this.data}));

    // Event binding.
    $('.rating', self.$el).on('click', function(e) { self.rate(self, this, e); });
    $('.favorite', self.$el).on('click', function(e) { self.favorite(self, this, e); });

    return this.$el;
}

var Thumbnail = function() {
    Wallpaper.apply(this, arguments);
}

Thumbnail.prototype = Object.create(Wallpaper.prototype);
Thumbnail.prototype.constructor = Thumbnail;

Thumbnail.prototype.hoverIn = function(self, that, e) {
    $('.meta', self.$el).show();
}

Thumbnail.prototype.hoverOut = function(self, that, e) {
    $('.meta', self.$el).hide();
}

Thumbnail.prototype.render = function() {
    var self = this;
    Wallpaper.prototype.render.call(this);

    this.$el.on('mouseover', function(e) { self.hoverIn(self, this, e); });
    this.$el.on('mouseout', function(e) { self.hoverOut(self, this, e); });

    return this.$el;
}