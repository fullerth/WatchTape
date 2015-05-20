var initialize = function(froogaloop, urls) {
    $('#id_jam_time_button').on('click', function() {
        froogaloop.api('CurrentTime')
        $.post(urls.video_to_jam, {'time' : 'data'})
    })
}

window.WatchTape = {
    VideoPlayer: {
        initialize: initialize
    }
}