test(
'initialize binds an #id_jam_time_button.onclick callback to \
froogaloop.api(\'CurrentTime\') object ', function() {
    var currentTimeWasCalled = false;
    var mockCurrentTimeFunction = function() {currentTimeWasCalled = true; };
    var mockFroogaloop = {
        api: function(method) {
            if(method = 'CurrentTime') { 
                mockCurrentTimeFunction()
            }
        }
    };
    
    WatchTape.VideoPlayer.initialize(mockFroogaloop);
    
    equal(currentTimeWasCalled, false, 
          'Check current time function is not called before click');
    $('#id_jam_time_button').trigger('click');
    equal(currentTimeWasCalled, true, 
          'Check current time function is called after click');
});

var token, requests, xhr;
module("id_jam_time_button onclick callback", {
    setup: function() {
        token = 'csrf token';
        mockFroogaloop = {
            api: sinon.mock()
        };
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
'initialize #id_jam_time_button onclick callback performs a $.post operation \
with the current time data from the video', function(){
    WatchTape.VideoPlayer.initialize(mockFroogaloop);
    console.log(requests)
    $('#id_jam_time_button').trigger('click');
    equal(requests.length, 1)
});