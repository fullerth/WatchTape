//Vimeo API onPlayProgress handler
current_jam = 0;
function play_tick(data, id)
{
    if(current_jam >= timing_data.length)
    {
        current_jam = timing_data.length
    }
    else
    {
        //currently simply changing 30 seconds behind. This will be a slightly
        //random timing for jams with timeouts or injury
        while((timing_data[current_jam]-4.5) < data.seconds)
        {
            //print("incrementing current jam")
            current_jam++;
        }
        var jam_str = "Jam Number "
        document.getElementById('jam_number').textContent =
                    jam_str.concat(current_jam);
        var jam_carousel = $('.carousel').carousel()
        jam_carousel.carousel(current_jam)
    }
}

function reset_jam(data, id) {
    current_jam = 0;
}

var froogaloop;

//Setup for video player page
$(document).ready(function() {
    // Vimeo player setup
    // Listen for the ready event for any vimeo video players on the page
    var player = $('#id_vimeo_player')[0];
    $f(player).addEvent('ready', ready);

    function addEvent(element, eventName, callback) {
        if (element.addEventListener) {
            element.addEventListener(eventName, callback, false);
        }
        else {
            element.attachEvent(eventName, callback, false);
        }
    }

    function ready(player_id) {
        console.log('ready!');
        window.froogaloop = $f(player_id);

        function onPlay() {
                window.froogaloop.addEvent('play', function(data) {
                    console.log('play');
                });
        }


        function setupResets() {
                window.froogaloop.addEvent('finish', reset_jam);
                window.froogaloop.addEvent('seek', reset_jam)
        }

        function onPlayProgress() {
            window.froogaloop.addEvent('playProgress', play_tick);
        }

        function set_starting_time() {
            window.froogaloop.api('seekTo',timing_data[0]-4.5)
        }

        onPlay();
        setupResets();
        onPlayProgress();
        set_starting_time();
        
        
        //Button control initialization
        urls = {'video_to_jam' : '/watchtape/videotojam/'};    
        WatchTape.VideoPlayer.initialize(window.froogaloop, urls);
    }
    
    
});
