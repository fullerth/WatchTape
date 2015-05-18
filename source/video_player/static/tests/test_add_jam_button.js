test('initialize binds a WatchTape.VideoPlayer object with froogaloop defined', function() {
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
    $('#id_jam_time').trigger('click');
    equal(currentTimeWasCalled, true, 
          'Check current time function is called after click');
});
