var urlButton = document.getElementById('start_analysis');
const paragraph = document.getElementById('analytics_report');
//var output = document.getElementById('output');
var url;
var data;

urlButton.onclick = function() {
      // Re-use the variables outside of this scope to retrieve 
      chrome.tabs.query({active: true,
        currentWindow: true}, function (tabs) {
    		//console.log(tabs[0].url.toString())

    		url = tabs[0].url.toString();

        //paragraph.innerHTML       = 'Processing url...'
        var socket                = io.connect('http://localhost:5000');

        socket.on('connect',function(){
          socket.emit('link', {link: url});
          console.log(url);
        });
        socket.on('analytics_report', function(data){
          console.log(data);
          paragraph.innerHTML = data.title.emotion.emotion_score;;
        })
  	});
};

