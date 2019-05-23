var urlButton = document.getElementById('getUrl');
var output = document.getElementById('output');
var url;
var data;

// var socket = chrome.socket || chrome.experimental.socket;
// client.connect(8484, '127.0.0.1', function() {
//     console.log('Connected');
//     socket.write('Hello, server! Love, Client.');
// });

// client.on('data', function(data) {
//     console.log('Received: ' + data);
//     socket.destroy(); // kill client after server's response
// });

// function encode_utf8(s) {
// 	return unescape(encodeURIComponent(s));
// }



urlButton.onclick = function() {
	  
    // Re-use the variables outside of this scope to retrieve 
    chrome.tabs.query({active: true,
      currentWindow: true}, function (tabs) {
  		//console.log(tabs[0].url.toString())

  		url = tabs[0].url.toString();
  		//child.stdin.write(url+"\n");
  		//data = encode_utf8(url)
  		console.log("url");
      console.log(url);
      var socket = io.connect('http://localhost:5000');
      socket.on('connect',function(){
        socket.emit('link', {link: url});
      });
      socket.on('reputation', function(data){
        const paragraph = document.getElementById('reputation');
        paragraph.innerHTML = data.grammar_mistakes;
      })
	});
};

