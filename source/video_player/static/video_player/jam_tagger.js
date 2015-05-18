var initialize = function(froogaloop) {
    $('#id_jam_time_button').on('click', function() {
        froogaloop.api('CurrentTime')
    })
}

window.WatchTape = {
    VideoPlayer: {
        initialize: initialize
    }
}