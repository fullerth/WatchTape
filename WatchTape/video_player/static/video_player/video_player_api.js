//Vimeo API onPlayProgress handler
function play_tick() {
    console.log('play_tick called');
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