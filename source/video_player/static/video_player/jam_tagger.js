var initialize = function(froogaloop) {
    $('#id_jam_time_button').on('click', function() {
        froogaloop.api('CurrentTime')
        $.post('/')
    })
}

window.WatchTape = {
    VideoPlayer: {
        initialize: initialize
    }
}