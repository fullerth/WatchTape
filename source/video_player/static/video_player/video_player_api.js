var VideoPlayer = {}

//Vimeo API onPlayProgress handler
var current_jam = 0;
function play_tick(data, id)
{
    try
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
    catch (e)
    {
        console.log(e)        
    }
}

function reset_jam(data, id) {
    current_jam = 0;
}

function create_new_jam() {
    retVal = $.post('watchtape/videotojam/')
    console.log(retVal)
}

//Setup for Vimeo API
$(document).ready(function() {
    // Listen for the ready event for any vimeo video players on the page
    var player = $('#vimeo_player')[0];
    if(player) {
        $f(player).addEvent('ready', ready);
    }

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
        VideoPlayer.froogaloop = $f(player_id);
        
        function onPlay() {
                VideoPlayer.froogaloop.addEvent('play', function(data) {
                    console.log('play');
                });
        }

        function setupResets() {
                VideoPlayer.froogaloop.addEvent('finish', reset_jam);
                VideoPlayer.froogaloop.addEvent('seek', reset_jam);
        }

        function onPlayProgress() {
            VideoPlayer.froogaloop.addEvent('playProgress', play_tick);
        }

        function set_starting_time() {
            VideoPlayer.froogaloop.api('seekTo',timing_data[0]-10)
        }

        onPlay();
        setupResets();
        onPlayProgress();
        set_starting_time();
    }
});