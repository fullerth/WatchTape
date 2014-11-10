//Vimeo API onPlayProgress handler
var current_jam = 0;
var desired_jam = 0;
var froogaloop

function get_current_jam_number(data)
{
    jam = current_jam;
    while((timing_data[jam]-30) < data.seconds)
    {
        console.log('activated jam fixer for jam ' + jam)
        jam++;
    }
    return jam
}

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
        current_jam = get_current_jam_number(data)

        if(current_jam != desired_jam)
        {
            console.log('current jam is ' + current_jam +' and desired jam is ' + desired_jam)
//             current_jam = desired_jam
//             froogaloop.api('seekTo',timing_data[desired_jam])
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

function seek_video(data, id) {
    current_jam = get_current_jam_number(data)
    desired_jam = current_jam
}

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
                froogaloop.addEvent('seek', seek_video)
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

    //Disable playProgress event handler while shuffling jams
    froogaloop.addEvent('playProgress', null)

    desired_jam++;
    froogaloop.api('seekTo',timing_data[desired_jam])

    //Re-enable playProgress event handler after jam shuffling complete
    froogaloop.addEvent('playProgress', play_tick)

}

//Previous Jam Carousel Button Handlers
function prev_jam(data, id) {
    prev_jam_timeout = 3

    console.log("prev_jam pressed")
    //Disable playProgress event handler while shuffling jams
    froogaloop.addEvent('playProgress', null)

    if(desired_jam > 0)
    {
        //If the back button is pushed with 3 seconds of the start of the jam
        //Move to the previous jam, like a music player
        if(data.seconds < timing_data[desired_jam] + prev_jam_timeout)
        {
            desired_jam--;
        }
    }

    froogaloop.api('seekTo',timing_data[desired_jam])

    //Re-enable playProgress event handler after jam shuffling complete
    froogaloop.addEvent('playProgress', play_tick)
}
