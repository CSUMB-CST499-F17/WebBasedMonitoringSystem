//Sets the table visibility to false until the data has been emitted.
window.onload = function(){ 
}


var socket = io(window.location.hostname+':5000');
var portNumber=""
var suiteName="";
var hostName="";
var suite_information;
var nodePosition;
var nodes;
var rawGraphData;

socket.on('connect', function(){

});

socket.on('disconnect');

function getData(){
    hideAllForms(); 
    hostName=$('#hostName').val();
    portNumber=$('#portNumber').val();
  
    suite_information = setInterval(function() { socket.emit('data', {
        'hostName':hostName,
        'portNumber':portNumber
        });
    }, 3000);
}

function hideAllForms(){
    $("#dropdown").css('display','none');
    $("#form1").css('display','none');
    $("#form2").css('display','none');

}

function sumbitFormFunction(){ 
    $("#form1").css('display','none');
    $("#form2").css('display','inline-block');
}

function submitOldFormFunction(){
    $("#form2").css('display','none');
    $("#form1").css('display','inline-block');
}

function playSuite(){
    getData();
}

function pauseSuite(){
    clearInterval(suite_information); 
}

function refreshPage(){
    window.location.reload();
}

function stopSuite(){

    clearInterval(suite_information);
    hostName=$('#hostName').val();
    portNumber=$('#portNumber').val();
        socket.emit('stop_suite', {
            'hostName':hostName,
            'portNumber':portNumber
        });}

function getLastNodePosition(){
    return nodePosition;
}

function setLastNodePosition(position) {
    nodePosition = position;
}

function getLocalData(){ 
    
    hideAllForms();

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

function getNodes() {
    return nodes;
}

function setNodes(nodeData) {
    nodes = nodeData;
}

function getAllKeys() {
    return Object.keys(getNodes());
}

socket.on('summary_info',function(data){
    setNodes(data[1]);
    var allKeys = getAllKeys();
    var getSingleKey= allKeys[0];
    var stateTotals=data[0]["state totals"];
    var currentStates = data[0]["states"];
    var numOfStates = data[0]["states"].length;
    var cylc_tasks = {};
    rawGraphData = data[3];
    
    //If ran locally data[4] will not be defined
    if(data[4]!=undefined) {
        suiteName = data[4]["name"];
    }
    
    //set suiteName when rest of the data comin in
    $("#nameOfSuite").text(suiteName);

    //Respectively: white - 0, pink - 1, red - 2, khaki - 3, gold - 4, lime - 5, green - 6, deep-sky-blue - 7, blue - 8, light-gray - 9, gray - 10, black - 11
    var colors = {"white":"#FFFFFF", "pink":"#FF1493", "red":"#FF0000", "khaki":"#F0E68C", "gold":"#FFD700", "lime":"#00FF00", "green":"#008000", "deep-sky-blue":"#00BFFF", "blue":"#0000FF", "light-gray":"#D3D3D3", "gray":"#808080", "black":"#000000"};

    var svg = d3.select("body").select("#nodes");
    var nodeXPosition = 25;
    var nodeYPosition = 50;
    svg.selectAll("*").remove();
    console.log(currentStates);
    
    for(var node in currentStates) {
        var numOfNodes = d3.select("body").select("#nodes").selectAll("circle")[0].length;
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
                    switch(getNodes()[allKeys[node]]["state"]) {
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
                    switch(getNodes()[allKeys[node]]["state"]) {
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
                .text(getNodes()[allKeys[node]]["name"] + "\n" + getNodes()[allKeys[node]]["label"]);
        } else {
            svg.select("#div" + node).select("#node" + node)
                .attr("fill", function() {
                    switch(getNodes()[allKeys[node]]["state"]) {
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
                    switch(getNodes()[allKeys[node]]["state"]) {
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
                .text(getNodes()[allKeys[node]]["name"] + "\n" + getNodes()[allKeys[node]]["label"]);
        }
    }

    //guaranteed by our suite
    //TODO:just create these d3 objs dynamically
    /*d3.select("body").select("#nodeOne").text(getNodes()[allKeys[0]]["name"] +"     "+getNodes()[allKeys[0]]["state"]+ " "+getNodes()[allKeys[0]]["label"]);
    d3.select("body").select("#nodeTwo").text(nodes[allKeys[1]]["name"]+"   "+nodes[allKeys[1]]["state"]+ " "+nodes[allKeys[1]]["label"]);
    d3.select("body").select("#nodeThree").text(nodes[allKeys[2]]["name"]+" "+nodes[allKeys[2]]["state"]+ " "+nodes[allKeys[2]]["label"]);
    d3.select("body").select("#nodeFour").text(nodes[allKeys[3]]["name"] +" "+nodes[allKeys[3]]["state"]+ " "+nodes[allKeys[3]]["lable"]);
    d3.select("body").select("#nodeFive").text("state totals:" + stateTotals);
    d3.select("body").select("#nodeSix").text(allKeys);
    console.log(data);*/

    getTasks(nodes, allKeys, cylc_tasks);
    setStatesData(data);
    
    /**
     * Function: Display Task Number and the tasks running on it.
     **/    
    var c = 0;
    for(task in cylc_tasks){
        
        c++;
        number = c.toString();
        d3.select("body").select("#node" + number).text("TASK NUMBER " + task + ": \t\t" + cylc_tasks[task]) ;
    }
	

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

    // ************** Generate the tree diagram  *****************
    var margin = {top: 80, right: 120, bottom: 20, left: 120},
        width = 960 - margin.right - margin.left,
        height = 500 - margin.top - margin.bottom;

    d3.select("body").select("center").select("div").selectAll("*").remove();

    /////////////////////////////////////////////////////////////////////////////
    var graphNode, graphLink, svg3, graphNodes, graphLinks;

    function buildGraph() {
        svg3 = d3.select("body").select("center").select("div").append("svg")
            .attr("id", "tree")
            .attr("width", 1000)
            .attr("height", 1000);
    
        var force = d3.layout.force()
            .size([width, height])
            .linkDistance(100)
            .gravity(0)
            .charge(-60)
            .on("tick", tick);

        graphNodes = force.nodes();
        graphLinks = force.links();
        var nodeMap = {};
        
        var counter = -1;
        for(var potentialLink in rawGraphData[0]) {
        
            var randomXNumber = Math.floor((Math.random() * 400) + 100),
                randomYNumber = Math.floor((Math.random() * 300) + 100),
                randomXNumber2 = Math.floor((Math.random() * 400) + 100),
                randomYNumber2 = Math.floor((Math.random() * 300) + 100);
        
            var firstNode = rawGraphData[0][potentialLink][0],
                secondNode = rawGraphData[0][potentialLink][1];
        
            if(firstNode != undefined && firstNode != null) {
            
                var nodeState;
                if(nodeMap[firstNode] == undefined || nodeMap[firstNode] == null) {
                
                    if(data[1][firstNode] == undefined || data[1][firstNode] == null) {
                        nodeState = "runahead";
                    } else {
                        nodeState = data[1][firstNode]["state"];
                    }
                
                    nodeMap[firstNode] = {"x": randomXNumber, "y": randomYNumber, "name": firstNode, "state": nodeState};
                    graphNodes.push(nodeMap[firstNode])
                    counter += 1;
                }
                if(secondNode != undefined && secondNode != null && firstNode != secondNode) {
                    if(nodeMap[secondNode] == undefined || nodeMap[secondNode] == null) {
                        if(data[1][secondNode] == undefined || data[1][secondNode] == null) {
                            nodeState = "runahead";
                        } else {
                            nodeState = data[1][secondNode]["state"];
                        }
                    
                        nodeMap[secondNode] = {x: randomXNumber2, y: randomYNumber2, "name": secondNode, "state": nodeState};
                        graphNodes.push(nodeMap[secondNode])
                        counter += 1;
                    }
                    graphLinks.push({source: nodeMap[firstNode], target: nodeMap[secondNode]})
                }
            }
        }
        
        d3.values(graphNodes);
    
        graphLink = svg3.append("g").attr("class", "links").selectAll("line").data(graphLinks);
    
        graphLink.enter().append("line");
    
        graphNode = svg3.append("g").attr("class", "nodes").selectAll("circle").data(graphNodes);
    
        graphNode.enter().append("circle")
            .on("mouseover", mouseover).on("mouseout", mouseout)
            .attr("r", 25)
            .attr("fill", function(d) {
            switch(d.state) {
                case "runahead": return colors["blue"];
                case "held": return colors["gold"];
                case "queued": return colors["blue"];
                case "running": return colors["green"];
                case "failed": return colors["red"];
                default: return colors["black"];
            }
        }).attr("stroke", function(d) {
            switch(d.state) {
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
        });
        graphNode.append("title")
            .text(function(d) { return d.name; });
    
        force.start();
    
    }
        
    function tick() {
        graphLink.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        graphNode.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    }
    
    function mouseover() {
        console.log("Enlarged")
        d3.select(this).transition()
            .duration(500)
            .attr("r", 50);
    }
    
    function mouseout() {
        console.log("Normalized")
        d3.select(this).transition()
            .duration(500)
            .attr("r", 25);
    }
    
    buildGraph();
    
//////////////////////////////////////////////////////////////////////////////
});

/**
 * Function: displayTasks
 * Returns: void
 * Summary: Puts labels(key) in a dictionary with a list(value) of tasks running for each label.
 */
function getTasks(nodes, getAllKeys, cylc_tasks){

    var list = [];

    for(var i = 0; i < getAllKeys.length; i++){ 
        
        var label = nodes[getAllKeys[i]]['label'];
        var name = nodes[getAllKeys[i]]['name'];
        var state = nodes[getAllKeys[i]]['state'];
        
        if(!(label in cylc_tasks)){

            list.push(name);
            list.push(state);
            cylc_tasks[label] = list;
            list = [];
        }
        else{
            cylc_tasks[label].push(name);
            cylc_tasks[label].push(state);
        }
    }
}


/**
 * Function:setData
 * Returns: void
 * Summary: Checks if states are null (non-exsistent) and replaces them with a 0.
 *          Sets the HTML tags with JSON info, and sets visible to true.
 */

function setStatesData(data){


    var current_date = new Date().getTime()/1000;
    var last = data[0].last_updated;
    var last_updated = new Date(last*1000).toLocaleString();
    var sec = Math.round(current_date - last);   

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
    document.getElementById("seconds").innerHTML = sec;

    /**
     * Elements Visible
     */
    document.getElementById("information").style.visibility = "visible";
    document.getElementById("runahead").style.visibility = "visible";
    

}
