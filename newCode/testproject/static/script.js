window.onload = function(){ 
}


var socket = io(window.location.hostname+':5000');
var portNumber=""
var suiteName="";
var hostName="";
var suite_information;

socket.on('connect', function(){

});

socket.on('disconnect');

function getData(){
    
    hostName = document.getElementById('hostName').value;
    portNumber = document.getElementById('portNumber').value;
    suiteName = document.getElementById('suiteName').value;
  
    document.getElementById("test").innerHTML = "DATA SENT";

    suite_information = {
	'hostName':hostName,
        'portNumber':portNumber,
	'suiteName':suiteName

	}

    socket.emit('data', suite_information); 
}


