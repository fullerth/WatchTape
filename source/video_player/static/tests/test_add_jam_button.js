
var token, requests, xhr, urls;
module("id_jam_time_button onclick callback", {
    setup: function() {
        token = 'csrf token';
        mockFroogaloop = {
            api: sinon.stub()
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
    var videoTime = 22;
    var player_id = 1;
    var video_id = 3;
    mockFroogaloop.api.withArgs('getCurrentTime' \
        ).callsArgWith(1, videoTime, player_id);

    WatchTape.VideoPlayer.initialize(mockFroogaloop, urls, video_id);
    $('#id_jam_time_button').trigger('click');

    equal(requests.length, 1, 'check ajax request')
    equal(requests[0].url, urls.video_to_jam, 'check url')
    equal(requests[0].method, 'POST', 'check ajax request method')
    equal(requests[0].requestBody, 'start_time='+videoTime+"&video="+video_id,\
        'check ajax request data')
});

test(
'initialize #id_jam_time_button onclick callback puts resulting jam into jam \
list', function(){
    var videoTime = 50
    mockFroogaloop.api.withArgs('getCurrentTime').returns(videoTime);

    WatchTape.VideoPlayer.initialize(mockFroogaloop, urls);
    jam_list = $('#id_jam_list');

    items = jam_list.find('li')
    equal(items.length, 0, 'check jam list pre-click')

    $('#id_jam_time_button').trigger('click');

    items = jam_list.find('li')
    equal(items.length, 1, 'check jam list post-click')
});

