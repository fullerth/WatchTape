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
        while((timing_data[current_jam]-30) < data.seconds)
        {
            current_jam++;
        }
        var jam_str = "Jam Number "
        document.getElementById('jam_number').textContent =
                    jam_str.concat(current_jam);
        var jam_carousel = $('.carousel').carousel();
        jam_carousel.carousel(current_jam)
    }
}

function reset_jam(data, id) {
    current_jam = 0;
}

var froogaloop

//Setup for Vimeo API
$(document).ready(function() {
    // Listen for the ready event for any vimeo video players on the page
    var player = $('#vimeo_player')[0];
    $f(player).addEvent('ready', ready);

    function addEvent(element, eventName, callback) {
        if (element.addEventListener) {
            element.addEventListener(eventName, callback, false);
        }
        else {
            element.attachEvent(eventName, callback, false);
        }
    }//addEvent

    function ready(player_id) {
        console.log('ready!');
        froogaloop = $f(player_id);

        function onPlay() {
                froogaloop.addEvent('play', function(data) {
                });
        }


        function setupResets() {
                froogaloop.addEvent('finish', reset_jam);
                froogaloop.addEvent('seek', reset_jam)
        }

        function onPlayProgress() {
            froogaloop.addEvent('playProgress', play_tick);
        }

        function set_starting_time() {
            froogaloop.api('seekTo',timing_data[0]-10)
        }

        onPlay();
        setupResets();
        onPlayProgress();
        set_starting_time();
    }//Vimeo player ready

    document.getElementById("next_jam").onclick = next_jam;
    document.getElementById("prev_jam").onclick = prev_jam;

});

//Next Jam Carousel Button Handlers
function next_jam(data, id) {
    current_jam++;
    froogaloop.api('seekTo',timing_data[current_jam])
}

//Previous Jam Carousel Button Handlers
function prev_jam(data, id) {
    console.log("prev_jam pressed")
    if(current_jam > 0)
    {
        current_jam--;
        froogaloop.api('seekTo',timing_data[current_jam])
    }
}
