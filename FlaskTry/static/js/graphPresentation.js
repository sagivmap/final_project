var width = $("#my_dataviz").innerWidth(),
    height = $("#my_dataviz").innerHeight(),
    id_count = 1,
    tf_barrier = 100,
    aua_barrier = 365,
    mf_barrier = 20,
    fd_barrier = 12,
    msp = 0.5,
    node_radius = 5,
    nodes = [{ "id": 0, "name": "Ego Node", "TF": "", "AUA": "", "CF": [], "MF": [], "FD": [], "Weight": -1, "TSP": -1, "level": 0 }],
    links = [],
    getXloc = d3.scalePoint().domain([0, 1, 2]).range([100, width - 100]);

var simulation = d3.forceSimulation(nodes)
    .force('x', d3.forceX((d) => getXloc(d.level)).strength(4))
    .force('collide', d3.forceCollide(node_radius*4))
    .force('charge', d3.forceManyBody().strength(0))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('link', d3.forceLink().links(links))
    .on('tick', ticked);

//drag handler
//d is the node
function drag_start(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function drag_drag(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function drag_end(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

var drag_handler = d3.drag()
    .on("start", drag_start)
    .on("drag", drag_drag)
    .on("end", drag_end);

// add 1 to id_count
function increase_id_count(){
    id_count++;
}
// node and link weight calculator
var calc_node_weight = function (TF, AUA) {
    var c_TF, c_AUA;
    if (TF > tf_barrier) { c_TF = 1; }
    else { c_TF = TF / tf_barrier; }
    if (AUA > aua_barrier) { c_AUA = 1; }
    else { c_AUA = AUA / aua_barrier; }
    return (c_TF + c_AUA) / 2;
}
var calc_link_weight = function (MF, FD) {
    var c_MF, c_FD;
    if (MF > mf_barrier) { c_MF = 1; }
    else {c_MF = MF / mf_barrier;}
    if (FD > fd_barrier) { c_FD = 1; }
    else {c_FD = FD / fd_barrier; }
    return (c_MF + c_FD) / 2;
}

// add find remove of nodes and links in DS
function removeNode(name) {
    nodes = _.filter(nodes, function (node) { return (node["name"] != name) });
    links = _.filter(links, function (link) { return ((link["source"]["name"] != name) && (link["target"]["name"] != name)) });
    update();
}

function findNode(Id) {
    for (var i in nodes) if (nodes[i]["id"] === Id) return nodes[i];
}

function findLink(source, target) {
    for (var i in links) {
        if (links[i]["source"]["id"] === source && links[i]["target"]["id"] === target)
            return links[i];
    }
}

function calculateLevel(CF) {
    if (CF.includes('0')) { return 1; }
    else { return 2; }
}

function addNode(Name, TF, AUA, CF, MF, FD) {
    var node_weight = calc_node_weight(TF, AUA),
        lvl = calculateLevel(CF);
 
    nodes.push({
        "id": id_count, "name": Name, "TF": TF, "AUA": AUA, "CF": CF, "MF": MF, "FD": FD,
        "Weight": node_weight, "TSP": -1, 'level': lvl
    });

}

var get_first_circle_link_weight = function (source_as_target) {
    return findLink(0, source_as_target)['Weight'];
}

function addLink(source, i) {
    var target_node = findNode(id_count);
    var link_weight = calc_link_weight(target_node['MF'][i], target_node['FD'][i]);
    var source_node = findNode(source);
    links.push({
        "source": source_node, "target": target_node,
        "MF": target_node['MF'][i], "FD": target_node['FD'][i], "Weight": link_weight
    });

    if (source > 0) {
        first_circle_link_weight = get_first_circle_link_weight(source);
        tsp_to_add = target_node['Weight'] * link_weight * source_node['Weight'] * first_circle_link_weight;
        if (tsp_to_add > target_node['TSP'])
            target_node['TSP'] = tsp_to_add;
    }
}

function update() {
    var link = d3.select('.links')
        .selectAll('line.link')
        .data(links).enter().insert("line")
        .attr("class", "link")
        .attr("x1", function (d) { return d.source.x; })
        .attr("y1", function (d) { return d.source.y; })
        .attr("x2", function (d) { return d.target.x; })
        .attr("y2", function (d) { return d.target.y; });

    link.exit().remove();

    node = d3.select('.nodes')
        .selectAll('g.node')
        .data(nodes).enter().append("g")
        .attr("class", "node");

    node.append("circle")
        .style("fill", function (d) {
            if (d.id == 0) { return "#0099ff" }
            if (d.CF.includes('0')) { return "#00cc00" }
            if (d.TSP > 0.5) { return "#ff9900" } else { return "#ff0000" }
        })
        .attr("r", 5);

    node.append("text")
        .attr("class", "nodetext")
        .attr("x", "0em")
        .attr("y", 15)
        .text(function (d) { return d.name });

    node.on("mouseover", function (d) {
        var g = d3.select(this); // The node
        // The class is used to remove the additional text later
        var info = g.append('text')
            .classed('info', true)
            .attr('dx', "0em")
            .attr('dy', -10)
            .text(function (d) {
                if (d.id == 0) { return "id=0" }
                else { return "id=" + d.id.toString() + ",TF=" + d.TF.toString() + ",AUA=" + d.AUA.toString() }
            })
            .style("font-size", "12px");
    }).on("mouseout", function () {
        // Remove the info text on mouse out.
        d3.select(this).select('text.info').remove()
    });


    node.exit().remove();

    drag_handler(node);
    simulation.nodes(nodes);
    simulation.force("link").links(links);
    simulation.alpha(1).restart();
}


function ticked() {
    var link = d3.select('.links')
        .selectAll('line.link')
        .data(links);
    link.attr("x1", function (d) { return d.source.x; })
        .attr("y1", function (d) { return d.source.y; })
        .attr("x2", function (d) { return d.target.x; })
        .attr("y2", function (d) { return d.target.y; });


    node = d3.select('.nodes')
        .selectAll('g.node')
        .data(nodes);

    node.attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")"; });
}

update();


function addNodeToGraph() {
    var name = document.getElementById("NodeName").value,
        tf = document.getElementById("TF").value,
        aua = document.getElementById("AUA").value,
        cf = document.getElementById("CF").value.split(","),
        mf = document.getElementById("MF").value.split(","),
        fd = document.getElementById("FD").value.split(",");

    addNode(name, tf, aua, cf, mf, fd);
    var i;
    for (i = 0; i < cf.length; i++) {
        addLink(parseInt(cf[i]), i);
    }
    increase_id_count();
    console.log(nodes);
    console.log(links);
    update();
}
