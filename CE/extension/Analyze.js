// // Socket
// var app = require('express')();
// var http = require('http').Server(app);
//var exampleSocket = new WebSocket("127.0.0.1", "8484");

// Start the main app logic.
//requirejs(['jquery', 'canvas', 'app/sub'],
//function   ($,        canvas,   sub) {
    //jQuery, canvas and the app/sub module are all
    //loaded and can be used here now.
//});
//var net = require('net');

// function urlFunction(){
// 	chrome.tabs.query({active: true,
//     currentWindow: true}, function (tabs) {
//   		//console.log(tabs[0].url.toString())

//   		var url = tabs[0].url.toString();
//   		//child.stdin.write(url+"\n");
//   		console.log("Current Url");
//   		console.log(url);
//   		return url;
  		
// 	});
// 	return url;
// }

var urlButton = document.getElementById('getUrl');
var output = document.getElementById('output');
var url;
var data;
websocket = new WebSocket('ws://localhost:12345');
function encode_utf8(s) {
	return unescape(encodeURIComponent(s));
}

urlButton.onclick = function() {
	
    // Re-use the variables outside of this scope to retrieve 
    chrome.tabs.query({active: true,
    currentWindow: true}, function (tabs) {
  		//console.log(tabs[0].url.toString())

  		url = tabs[0].url.toString();
  		//child.stdin.write(url+"\n");
  		data = encode_utf8(url)
  		console.log("Current Data");
  		console.log(data);
  		websocket.onopen = () => websocket.send(data);	
	});
    //console.log("after click")
    //console.log(url)

    // Create the Socket
	//chrome.sockets.udp.create({}, function(socketInfo) {
  // The socket is created, now we can send some data
	 // 	chrome.socket.create(tcp,,function(object createInfo) {...})
	 // 	var socketId = socketInfo.socketId;
	 // 	chrome.sockets.send(socketId, arrayBuffer,
	  //  	'127.0.0.1', 3000, function(sendInfo) {
	   //  	 console.log("sent " + sendInfo.bytesSent);
	 //	});
	//});
    //var client = new net.Socket();
	//client.connect(8484, '127.0.0.1', function() {
   // 	console.log('Connected');
   // 	client.write('Hello, server! Love, Client.');
//	});
//	client.on('data', function(data) {
 //   	console.log('Received: ' + data);
  //  	client.destroy(); // kill client after server's response
//	});
    //output.value = urlFunction();
 //    app.get('/', function(req, res){
	// 	var url = urlFunction()
 //  		res.send(url);
	// });
    // Update the sum element with the result of the function
};








//http.listen(3000, function(){
//  console.log('listening on *:3000');