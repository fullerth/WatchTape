var initialize = function(froogaloop, urls) {
    $('#id_jam_time_button').on('click', function() {
        time = froogaloop.api('CurrentTime')
        resp = $.post(urls.video_to_jam, {'time' : time});
        console.log(resp);
    })
}

window.WatchTape = {
    VideoPlayer: {
        initialize: initialize
    }
}