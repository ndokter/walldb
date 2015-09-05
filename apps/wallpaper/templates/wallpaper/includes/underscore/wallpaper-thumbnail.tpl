<script id="wallpaper-thumbnail-template" type="text/template">
    <div class="thumbnail">
        <div class="meta img-rounded text-center">
            <div class="options">
                <a href="#" title="Favorite" class="favorite<% if (wallpaper.user_favorite) { %> active<% } %>">
                    <span class="glyphicon glyphicon-star"></span>
                </a>
                <a href="#" title="Upvote" class="rating upvote<% if (wallpaper.user_rating > 0) { %> active<% } %>" data-score-value="1">
                    <span class="glyphicon glyphicon-chevron-up"></span>
                </a>
                <a href="#" title="Downvote" class="rating downvote<% if (wallpaper.user_rating < 0) { %> active<% } %>" data-score-value="-1">
                    <span class="glyphicon glyphicon-chevron-down"></span>
                </a>
            </div>
            <span class="resolution"><%= wallpaper.width %> x <%= wallpaper.height %></span>
        </div>

        <a href="/wallpaper/<%= wallpaper.hash %>/" target="_blank">
            <img data-wallpaper-id="<%= wallpaper.hash %>" class="box-shadow img-rounded" src="<%= wallpaper.thumbnails[0].file %>" />
        </a>
    </div>
</script>