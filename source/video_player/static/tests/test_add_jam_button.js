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
