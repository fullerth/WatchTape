//Vimeo API onPlayProgress handler
current_jam = 0;
function play_tick(data, id) {
    if(current_jam == timing_data.length) {
        current_jam = timing_data.length
    }
    else if(timing_data[current_jam] < data.seconds) {
        current_jam++;
        console.log(current_jam)
    }
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
            }

            function ready(player_id) {
                console.log('ready!');
                var froogaloop = $f(player_id);

                function onPlay() {
                        froogaloop.addEvent('play', function(data) {
                            console.log('play');
                        });
                }


                function onFinish() {
                        froogaloop.addEvent('finish', function(data) {
                            console.log('finish');
                        });
                }

                function onPlayProgress() {
                    froogaloop.addEvent('playProgress', play_tick);
                }

                onPlay();
                onFinish();
                onPlayProgress();
            }
        });