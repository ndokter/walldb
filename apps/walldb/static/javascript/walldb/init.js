app = new WallDB();

app.on('route:main', function () {
    applicationMainView.render();
});

Backbone.history.start();
