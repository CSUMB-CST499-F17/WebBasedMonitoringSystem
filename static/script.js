//Sets the table visibility to false until the data has been emitted.
window.onload = function(){
    document.getElementById("information").style.visibility = "hidden";
    document.getElementById("table").style.visibility = "hidden";
    //document.getElementById("updated").style.visibility = "hidden";
}


var socket = io(window.location.hostname+':5000');
var portNumber=""
var suiteName="";
var hostName="";
var suite_information;
var nodePosition;
var paused_suite = false;



socket.on('connect', function(){

});

socket.on('disconnect');
function getData(){
    hostName=$('#hostName').val();
    portNumber=$('#portNumber').val();
    suite_information = setInterval(function() { socket.emit('data', {
        'hostName':hostName,
        'portNumber':portNumber
        });
    }, 3000);
}

function playSuite(){
    getData();
}

function pauseSuite(){
    clearInterval(suite_information);
    paused_suite = true;
}

function stopSuite(){

    if(paused_suite){
        
        clearInterval(suite_information);
        hostName=$('#hostName').val();
        portNumber=$('#portNumber').val();
            socket.emit('stop_suite', {
                'hostName':hostName,
                'portNumber':portNumber
            });
    }
}

function getLastNodePosition(){
    return nodePosition;
}

function setLastNodePosition(position) {
    nodePosition = position;
}
function getLocalData(){
    suiteName=$('#suiteName').val();
    socket.emit('getName', {
        'suiteName':suiteName
    });
    socket.on('name',function(data){


    if(data["portNumber"]!=undefined)
    {
      setInterval(function() {
          socket.emit('localData', {
              'portNumber':data['portNumber']
          });


      }, 3000);
    }
  })
}

socket.on('summary_info',function(data){
    var nodes=data[1];
    var getAllKeys = Object.keys(nodes);
    var getSingleKey= Object.keys(nodes)[0];
    var stateTotals=data[0]["state totals"];
    var currentStates = data[0]["states"];
    var numOfStates = data[0]["states"].length;

    //If ran locally data[3] will not be defined
    if(data[3]!=undefined)
    {
    suiteName = data[3]["name"];
  }
  //set suiteName when rest of the data comin in
  $("#nameOfSuite").text(suiteName);
    //console.log(suiteName);


    //Respectively: white - 0, pink - 1, red - 2, khaki - 3, gold - 4, lime - 5, green - 6, deep-sky-blue - 7, blue - 8, light-gray - 9, gray - 10, black - 11
    var colors = {"white":"#FFFFFF", "pink":"#FF1493", "red":"#FF0000", "khaki":"#F0E68C", "gold":"#FFD700", "lime":"#00FF00", "green":"#008000", "deep-sky-blue":"#00BFFF", "blue":"#0000FF", "light-gray":"#D3D3D3", "gray":"#808080", "black":"#000000"};

    var svg = d3.select("body").select("#nodes");
    var nodeXPosition = 25;
    var nodeYPosition = 50;
    svg.selectAll("*").remove();
    console.log(currentStates);
    for(var node in currentStates) {
        console.log(node);
        var numOfNodes = d3.select("body").select("#nodes").selectAll("circle")[0].length;
        console.log("Number of nodes: " + numOfNodes + "\nList size: " + numOfStates);
        if(numOfNodes < numOfStates) {
            if(numOfNodes == 0) {
                setLastNodePosition({"x":nodeXPosition, "y":nodeYPosition});
            } else {
                nodeXPosition += 50;
                setLastNodePosition({"x":nodeXPosition, "y":nodeYPosition});
            }
            var element = svg.append("g")
                .attr("id", "div" + node)
                .style("visibility", "visible");
            element.append("circle")
                .attr("id", "node" + node)
                .attr("cx", getLastNodePosition()["x"])
                .attr("cy", getLastNodePosition()["y"])
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
                .attr("x", getLastNodePosition()["x"] - 20)
                .attr("y", getLastNodePosition()["y"])
                .attr("font-size", "15px")
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
			d3.select("body").select("#nodeFour").text(nodes[getAllKeys[3]]["name"] +" "+nodes[getAllKeys[3]]["state"]+ " "+nodes[getAllKeys[3]]["label"]);
			d3.select("body").select("#nodeFive").text("state totals:" + stateTotals);
		   d3.select("body").select("#nodeSix").text(getAllKeys);
            console.log(data);
    
    displayTasks(nodes, getAllKeys);

    setStatesData(data);




    /**
     * Error Checking.
     */ 
    console.log("State totals", data[0]['state totals']);
    console.log("Obj0", data[0]);
    console.log("Nodes", data[1]);
    
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

/**
 * Function: displayTasks
 * Returns: void
 * Summary: Puts labels(key) in a dictionary with a list(value) of tasks running for each label.
 */
function displayTasks(nodes, getAllKeys){

    var list = [];
    var cylc_tasks = {};

    //console.log("KEYS", getAllKeys);  
   // console.log("Length", getAllKeys.length);
    
    
    for(var i = 0; i < getAllKeys.length; i++){ 
        
        var label = nodes[getAllKeys[i]]['label'];
        var name = nodes[getAllKeys[i]]['name'];
        var state = nodes[getAllKeys[i]]['state'];
        
        if(!(label in cylc_tasks)){
            
            //console.log("LABELin ", label);
            //console.log("Namein ", name);

            list.push(name);
            list.push(state);
            cylc_tasks[label] = list;
            list = [];
        }
        else{
            //console.log("Else");
            cylc_tasks[label].push(name);
            cylc_tasks[label].push(state);
        }
    }
   
  for(i in cylc_tasks){
    console.log("Key is" + i);

      console.log(typeof(cylc_tasks[i].length));

      for(var j = 0; j < cylc_tasks[i].length; j++){
        
          //Even == STATE
        if(j % 2 == 0){
            console.log("State: ",cylc_tasks[i][j]);
        }else{
            console.log("Label:", cylc_tasks[i][j]);
        }
      }
  }

  console.log("LIST:", cylc_tasks);  
}


/**
 * Function:setData
 * Returns: void
 * Summary: Checks if states are null (non-exsistent) and replaces them with a 0.
 *          Sets the HTML tags with JSON info, and sets visible to true.
 */

function setStatesData(data){

    last_updated = new Date(data[0].last_updated*1000);


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


    /**
     * Set HTML tags with JSON data.
     */
    document.getElementById("runahead").innerHTML = runahead;
    document.getElementById("waiting").innerHTML = waiting;
    document.getElementById("succeeded").innerHTML = succeeded;
    document.getElementById("running").innerHTML = running;
    document.getElementById("information").innerHTML = last_updated;

    /**
     * Elements Visible
     */
    document.getElementById("information").style.visibility = "visible";
    document.getElementById("table").style.visibility = "visible";
    document.getElementById("runahead").style.visibility = "visible";
    document.getElementById("updated").style.visibility = "visible"; 

}
