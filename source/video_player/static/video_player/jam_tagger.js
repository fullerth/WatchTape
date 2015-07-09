var initialize = function(froogaloop, urls) {
    $('#id_jam_time_button').on('click', function() {
        var time
        froogaloop.api('getCurrentTime', function(value, player_id){
            time = value
        })
        console.log(time)
        $.post(urls.video_to_jam, {'time' : time});

        append_list = $('#id_jam_list')
        new_item = $( "<li>New Item</li>" )
        new_item.appendTo("#id_jam_list")
    })
}

window.WatchTape = {
    VideoPlayer: {
        initialize: initialize
    }
}