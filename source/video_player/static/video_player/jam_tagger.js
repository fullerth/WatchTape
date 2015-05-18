var initialize = function(froogaloop) {
    $('#id_jam_time').on('click', function() {
        froogaloop.api('CurrentTime')
    })
}

window.WatchTape = {
    VideoPlayer: {
        initialize: initialize
    }
}