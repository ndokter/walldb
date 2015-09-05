<script id="wallpaper-detail-template" type="text/template">
    <div class="wallpaper">
        <div class="meta img-rounded text-center">
            <div class="options">
                <a href="#" title="Favorite" class="favorite<% if (wallpaper.user_favorite) { %> active<% } %>"><span class="glyphicon glyphicon-star"></span></a>
                <a href="#" title="Upvote" class="rating upvote<% if (wallpaper.user_rating > 0) { %> active<% } %>" data-score-value="1"><span class="glyphicon glyphicon-chevron-up"></span></a>
                <a href="#" title="Downvote" class="rating downvote<% if (wallpaper.user_rating < 0) { %> active<% } %>" data-score-value="-1"><span class="glyphicon glyphicon-chevron-down"></span></a>
            </div>
            <span class="resolution"><%= wallpaper.width %> x <%= wallpaper.height %></span>
            <a href="<%= wallpaper.file %>" download>download</a>
        </div>

        <img data-wallpaper-id="<%= wallpaper.hash %>" src="<%= wallpaper.file %>" />
    </div>
</script>