//Sets the table visibility to false until the data has been emitted.
window.onload = function(){
    document.getElementById("information").style.visibility = "hidden";
    document.getElementById("table").style.visibility = "hidden";
    document.getElementById("updated").style.visibility = "hidden";
    document.getElementById("stopSuiteButton").style.visibility = "hidden";
}

var socket = io('http://127.0.0.1:5000');
var hostName="";
var portNumber="";

socket.on('connect', function(){});
socket.on('disconnect');

function getData(){
    hostName=$('#hostName').val();
    portNumber=$('#portNumber').val();
    setInterval(function() { 
        socket.emit('data', {
            'hostName':hostName,
            'portNumber':portNumber
        });
    }, 3000);
}

last_updated="";
socket.on('summary_info',function(data){
    var nodes=data[1];
    var getAllKeys = Object.keys(nodes);
    var getSingleKey= Object.keys(nodes)[0];
    //console.log(data[getAllKeys[5]]);
    var stateTotals=data[0]["state totals"];
    
    //Respectively: white - 0, pink - 1, red - 2, khaki - 3, gold - 4, lime - 5, green - 6, deep-sky-blue - 7, blue - 8, light-gray - 9, gray - 10, black - 11
    var colors = {"white":"#FFFFFF", "pink":"#FF1493", "red":"#FF0000", "khaki":"#F0E68C", "gold":"#FFD700", "lime":"#00FF00", "green":"#008000", "deep-sky-blue":"#00BFFF", "blue":"#0000FF", "light-gray":"#D3D3D3", "gray":"#808080", "black":"#000000"};

    
    var svg = d3.select("body").select("#nodes");
    var nodeXPosition = 0;
    var nodeYPosition = 50;
    for(var node in getAllKeys) {
        nodeXPosition += 50;
        var numOfNodes = d3.select("body").select("#nodes").selectAll("circle")[0].length;
        console.log("Number of nodes: " + numOfNodes + "\nList size: " + getAllKeys.length);
        if(numOfNodes < getAllKeys.length) {
            var element = svg.append("g")
                .attr("id", "div" + node)
                .style("visibility", "visible");
            element.append("circle")
                .attr("id", "node" + node)
                .attr("cx", nodeXPosition)
                .attr("cy", nodeYPosition)
                .attr("r", "25")
                .attr("fill", function() {
                    switch(nodes[getAllKeys[node]]["state"]) {
                        case "runahead": return colors["blue"];
                        case "held": return colors["gold"];
                        case "queued": return colors["blue"];
                        case "running": return colors["green"];
                        case "failed": return colors["red"];
                        default: return colors["black"];
                    }
                });
            element.append("text")
                .attr("id", "text" + node)
                .attr("x", nodeXPosition - 20)
                .attr("y", nodeYPosition)
                .attr("font-size", "15px")
                .style("fill", function() {
                    console.log("Style should work")
                    switch(nodes[getAllKeys[node]]["state"]) {
                        case "runahead": return colors["light-gray"];
                        case "waiting": return colors["deep-sky-blue"];
                        case 'held': return colors["gray"];
                        case 'queued': return colors["white"];
                        case 'ready': return colors["lime"];
                        case 'expired': return colors["light-gray"];
                        case 'submitted': return colors["khaki"];
                        case 'submit-failed': return colors["blue"];
                        case 'submit-retrying': return colors["red"];
                        case 'running': return colors["light-gray"];
                        case 'succeeded': return colors["white"];
                        case 'failed': return colors["light-gray"];
                        case 'retrying': return colors["pink"];
                        default: return colors["white"];
                    }
                })
                .text(nodes[getAllKeys[node]]["name"] + "\n" + nodes[getAllKeys[node]]["label"]);
        } else {
            svg.select("#div" + node).select("#node" + node)
                .attr("fill", function() {
                    switch(nodes[getAllKeys[node]]["state"]) {
                        case "runahead": return colors["blue"];
                        case "held": return colors["gold"];
                        case "queued": return colors["blue"];
                        case "running": return colors["green"];
                        case "failed": return colors["red"];
                        default: return colors["black"];
                    }
                });
            svg.select("#div" + node).select("#text" + node)
                .style("fill", function() {
                    switch(nodes[getAllKeys[node]]["state"]) {
                        case "runahead": return colors["light-gray"];
                        case "waiting": return colors["deep-sky-blue"];
                        case 'held': return colors["gray"];
                        case 'queued': return colors["white"];
                        case 'ready': return colors["lime"];
                        case 'expired': return colors["light-gray"];
                        case 'submitted': return colors["khaki"];
                        case 'submit-failed': return colors["blue"];
                        case 'submit-retrying': return colors["red"];
                        case 'running': return colors["light-gray"];
                        case 'succeeded': return colors["white"];
                        case 'failed': return colors["light-gray"];
                        case 'retrying': return colors["pink"];
                        default: return colors["white"];
                    }
                })
                .text(nodes[getAllKeys[node]]["name"] + "\n" + nodes[getAllKeys[node]]["label"]);
        }
    }
        //guaranteed by our suite
		//TODO:just create these d3 objs dynamically
			d3.select("body").select("#nodeOne").text(nodes[getAllKeys[0]]["name"] +" "+nodes[getAllKeys[0]]["state"]+ " "+nodes[getAllKeys[0]]["label"]);
		  d3.select("body").select("#nodeTwo").text(nodes[getAllKeys[1]]["name"]+" "+nodes[getAllKeys[1]]["state"]+ " "+nodes[getAllKeys[1]]["label"]);
			d3.select("body").select("#nodeThree").text(nodes[getAllKeys[2]]["name"]+" "+nodes[getAllKeys[2]]["state"]+ " "+nodes[getAllKeys[2]]["label"]);
			d3.select("body").select("#nodeFour").text(nodes[getAllKeys[3]]["name"] +" "+nodes[getAllKeys[3]]["state"]+ " "+nodes[getAllKeys[3]]["lable"]);
			d3.select("body").select("#nodeFive").text("state totals:" + stateTotals);
		   d3.select("body").select("#nodeSix").text(getAllKeys);
            console.log(data);


    //Get information from suite every interval.
    last_updated = data[0].last_updated;
    runahead = data[0]['state totals'].runahead;
    if(runahead == null | runahead == undefined){
			runahead = "0";
    }
    waiting = data[0]['state totals'].waiting;
    if(waiting == null | waiting == undefined){
        waiting = "0";
    }
    succeeded = data[0]['state totals'].succeeded;
    if(succeeded == null | succeeded == undefined){
        succeeded = "0";
    }
    running = data[0]['state totals'].running;
    if(running == null | running == undefined){
        running = "0";
    }

    //Set element to the data from the JSON.
    document.getElementById("information").innerHTML = last_updated;
    document.getElementById("runahead").innerHTML = runahead;
    document.getElementById("waiting").innerHTML = waiting;
    document.getElementById("succeeded").innerHTML = succeeded;
    document.getElementById("running").innerHTML = running;


    //Output to the console. Error fixing.
    console.log("State totals", data[0]['state totals']);
    console.log("RUNAHEAD", data[0]["state totals"].runahead);
    console.log("SUCCEEDED", data[0]["state totals"].succeeded);
    console.log("OB2", data[1]['state']);
    console.log("OBJ3 ", data[2]);


    //Make all Elements Visible.
    document.getElementById("information").style.visibility = "visible";
    document.getElementById("table").style.visibility = "visible";
    document.getElementById("runahead").style.visibility = "visible";
    document.getElementById("updated").style.visibility = "visible";
    document.getElementById("stopSuiteButton").style.visibility = "visible";
    
    //$('ul').html(buffer);
    
    var th_elements = d3.select("body").select("table").select("tr").selectAll("th");
    
    for(var element in th_elements[0]) {
        switch(th_elements[0][element].textContent.trim()) {
            case 'runahead': th_elements[0][element].style.backgroundColor = colors["blue"];
                th_elements[0][element].style.color = colors["light-gray"];
                break;
            case 'waiting': th_elements[0][element].style.backgroundColor = colors["black"];
                th_elements[0][element].style.color = colors["deep-sky-blue"];
                break;
            case 'held': th_elements[0][element].style.backgroundColor = colors["gold"];
                th_elements[0][element].style.color = colors["gray"];
                break;
            case 'queued': th_elements[0][element].style.backgroundColor = colors["blue"];
                th_elements[0][element].style.color = colors["white"];
                break;
            case 'ready': th_elements[0][element].style.backgroundColor = colors["black"];
                th_elements[0][element].style.color = colors["lime"];
                break;
            case 'expired': th_elements[0][element].style.backgroundColor = colors["black"];
                th_elements[0][element].style.color = colors["light-gray"];
                break;
            case 'submitted': th_elements[0][element].style.backgroundColor = colors["black"];
                th_elements[0][element].style.color = colors["khaki"];
                break;
            case 'submit-failed': th_elements[0][element].style.backgroundColor = colors["black"];
                th_elements[0][element].style.color = colors["blue"];
                break;
            case 'submit-retrying': th_elements[0][element].style.backgroundColor = colors["black"];
                th_elements[0][element].style.color = colors["red"];
                break;
            case 'running': th_elements[0][element].style.backgroundColor = colors["green"];
                th_elements[0][element].style.color = colors["light-gray"];
                break;
            case 'succeeded': th_elements[0][element].style.backgroundColor = colors["black"];
                th_elements[0][element].style.color = colors["white"];
                break;
            case 'failed': th_elements[0][element].style.backgroundColor = colors["red"];
                th_elements[0][element].style.color = colors["light-gray"];
                break;
            case 'retrying': th_elements[0][element].style.backgroundColor = colors["black"];
                th_elements[0][element].style.color = colors["pink"];
                break;
            default:
                break;
            }
        }
});