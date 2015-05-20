var token, requests, xhr, urls;
module("id_jam_time_button onclick callback", {
    setup: function() {
        token = 'csrf token';
        mockFroogaloop = {
            api: sinon.mock()
        };
        urls = { video_to_jam : 'video_to_jam'}
        xhr = sinon.useFakeXMLHttpRequest();
        requests = []
        xhr.onCreate = function(request) {requests.push(request)};
    },
    teardown: function() {
        mockFroogaloop.api.reset();
        xhr.restore();
    }
})

test(
'initialize binds an #id_jam_time_button.onclick callback that calls the \
froogaloop.api(\'CurrentTime\') object', function() {    
    WatchTape.VideoPlayer.initialize(mockFroogaloop, urls);
    
    $('#id_jam_time_button').trigger('click');
    
    ok(mockFroogaloop.api.calledOnce, 'check add jam button logic');
});


test(
'initialize #id_jam_time_button onclick callback performs a $.post operation \
with the current time data from the video', function(){
    WatchTape.VideoPlayer.initialize(mockFroogaloop, urls);
    $('#id_jam_time_button').trigger('click');
    equal(requests.length, 1, 'check ajax request')
    equal(requests[0].url, urls.video_to_jam, 'check url')
});