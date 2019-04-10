var width = $("#svg-id").innerWidth(),
    height = $("#svg-id").innerHeight(),
    id_count = 1,
    tf_barrier = 100,
    aua_barrier = 365,
    mf_barrier = 20,
    fd_barrier = 12,
    msp = 0.5,
    r = 5,
    nodes = [{ "id": 0, "name": "Ego Node", "TF": "", "AUA": "", "CF": [], "MF": [], "FD": [], "Weight": -1, "TSP": -1, "level": 0 }],
    bad_nodes = new Set([]),
    links = [],
    bad_links = new Set([]),
    getXloc = d3.scalePoint().domain([0, 1, 2]).range([100, width - 100]),
    there_are_bad_connections = false,
    show_bad_connections = false;

var simulation = d3.forceSimulation(nodes)
    .force('x', d3.forceX((d) => getXloc(d.level)).strength(4))
    .force('collide', d3.forceCollide(r*4))
    .force('charge', d3.forceManyBody().strength(0))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('link', d3.forceLink().links(links).id(function (d) { return d.id }))
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

function get_all_low_tsp_second_level_nodes() {
    var nodes_to_return = [];
    for (var i in nodes) {
        if (nodes[i]["level"] === 2 && nodes[i]["TSP"] < msp) {
            nodes_to_return.push(JSON.parse(JSON.stringify(nodes[i])));
        }
    }
    return nodes_to_return;
}

function get_first_circle_nodes_and_links_of_second(id_of_second) {
    var nodes_to_return = [];
    var links_to_return = [];
    for (var i in links) {
        if (links[i]["target"]["id"] === id_of_second) {
            nodes_to_return.push(JSON.parse(JSON.stringify(links[i]["source"])));
            links_to_return.push(JSON.parse(JSON.stringify(links[i])));
        }
    }
    return [nodes_to_return, links_to_return]
}


function findLink(source, target) {
    for (var i in links) {
        if (links[i]["source"]["id"] === source && links[i]["target"]["id"] === target)
            return links[i];
    }
}

function calculateLevel(CF) {
    if (CF.includes(0)) { return 1; }
    else { return 2; }
}

function getLevelPerId(id) {
    for (var i in nodes) if (nodes[i]["id"] === id) return nodes[i]["level"];
}

function validateAddNodeLevels(lvl, CF) {
    if (lvl === 2) {
        for (i = 0; i < CF.length; i++) {
            if (getLevelPerId(CF[i]) === 2) {
                window.alert("Adding 2nd circle node can be linked only to 1st circle nodes");
                return false;
            }
        }
    }
    return true;
}

function addNode(Name, TF, AUA, CF, MF, FD) {
    var node_weight = calc_node_weight(TF, AUA),
        lvl = calculateLevel(CF);
    if (validateAddNodeLevels(lvl, CF)) {
        nodes.push({
            "id": id_count, "name": Name, "TF": TF, "AUA": AUA, "CF": CF, "MF": MF, "FD": FD,
            "Weight": node_weight, "TSP": -1, 'level': lvl
        });
        return true;
    }
    return false;
}

var get_first_circle_link_weight = function (source_as_target) {
    return findLink(0, source_as_target)['Weight'];
}

function addLink(source, i) {
    var target_node = findNode(id_count);
    var link_weight = calc_link_weight(target_node['MF'][i], target_node['FD'][i]);
    var source_node = findNode(source);

    links.push({
        "source": source_node.id, "target": target_node.id,
        "MF": target_node['MF'][i], "FD": target_node['FD'][i], "Weight": link_weight
    });


    if (source > 0) {
        first_circle_link_weight = get_first_circle_link_weight(source);
        tsp_to_add = target_node['Weight'] * link_weight * source_node['Weight'] * first_circle_link_weight;
        if (tsp_to_add > target_node['TSP']) {
            target_node['TSP'] = tsp_to_add;
            if (tsp_to_add < msp)
                there_are_bad_connections = true;
            
        }
    }
}

function update() {

    var link = d3.select('.links')
        .selectAll('line.link')
        .data(show_bad_connections ? bad_links : links).enter().insert("line")
        .attr("class", "link")
        .attr("x1", function (d) { return d.source.x; })
        .attr("y1", function (d) { return d.source.y; })
        .attr("x2", function (d) { return d.target.x; })
        .attr("y2", function (d) { return d.target.y; });

    link.exit().remove();

    node = d3.select('.nodes')
        .selectAll('g.node')
        .data(show_bad_connections ? bad_nodes : nodes).enter().append("g")
        .attr("class", "node");

    node.append("circle")
        .style("fill", function (d) {
            if (d.id == 0) { return "#0099ff" }
            if (d.CF.includes(0)) { return "#00cc00" }
            if (d.TSP > 0.5) { return "#ff9900" } else { return "#ff0000" }
        })
        .attr("r", r);

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

        d3.selectAll('line.link')
            .filter(function (l) {
                return (d.id != 0 && (d.id == l.source.id || d.id == l.target.id));
            })
            .style("opacity", 1)

    }).on("mouseout", function () {
        d3.selectAll('line.link').style("opacity", 0.1)
        // Remove the info text on mouse out.
        d3.select(this).select('text.info').remove();
        
    });

    node.exit().remove();

    drag_handler(node);
    simulation.nodes(show_bad_connections ? bad_nodes : nodes);
    simulation.force("link").links(show_bad_connections ? bad_links : links).id(function (d) { return d.id });
    simulation.on('tick', ticked)
    simulation.alpha(1).restart();
}


function ticked() {
    var link = d3.select('.links')
        .selectAll('line.link')
        .data(show_bad_connections ? bad_links : links);
    link.attr("x1", function (d) { return d.source.x; })
        .attr("y1", function (d) { return d.source.y; })
        .attr("x2", function (d) { return d.target.x; })
        .attr("y2", function (d) { return d.target.y; });


    node = d3.select('.nodes')
        .selectAll('g.node')
        .data(show_bad_connections ? bad_nodes : nodes);

    node.attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")"; });
}

update();

function cfIdIsLargerThenNodesLen(cf) {
    var i;
    for (i = 0; i < cf.length; i++) {
        if (cf[i] >= nodes.length) {
            window.alert("No such node: " + cf[i].toString());
            return true;
        }
    }
    return false;
}

function checkIfCfCorrect(cf) {
    if (cf.includes(0) && cf.length > 1) {
        window.alert("Adding link to Ego node, cannot add to more nodes");
        return false;
    } else if (cfIdIsLargerThenNodesLen(cf)){
        return false;
    }
    return true;
}

function addNodeToGraph() {
    var name = document.getElementById("NodeName").value,
        tf = parseInt(document.getElementById("TF").value),
        aua = parseInt(document.getElementById("AUA").value),
        cf = document.getElementById("CF").value.split(",").map(function (num) { return parseInt(num, 10); }),
        mf = document.getElementById("MF").value.split(",").map(function (num) { return parseInt(num, 10); }),
        fd = document.getElementById("FD").value.split(",").map(function (num) { return parseInt(num, 10); });
    if (checkIfCfCorrect(cf)) {
        if (addNode(name, tf, aua, cf, mf, fd)) {
            var i;
            for (i = 0; i < cf.length; i++) {
                addLink(cf[i], i);
            }
            increase_id_count();
            update();
        }
    }
}

function show_only_bad_connections() {
    if (!there_are_bad_connections)
        window.alert("All connections are GOOD connections!")
    else {
        bad_links = new Set([]);
        second_level_nodes_with_low_tsp = new Set(get_all_low_tsp_second_level_nodes());
        bad_nodes = new Set([...bad_nodes, ...second_level_nodes_with_low_tsp]);
        for (let item of second_level_nodes_with_low_tsp) {
            first_circle_nodes_and_links_of_bad_node = get_first_circle_nodes_and_links_of_second(item['id']);
            first_circle_nodes = new Set(first_circle_nodes_and_links_of_bad_node[0]);
            second_circle_links = new Set(first_circle_nodes_and_links_of_bad_node[1]);
            bad_nodes = new Set([...bad_nodes, ...first_circle_nodes]);
            bad_links = new Set([...bad_links, ...second_circle_links]);
            for (let node of first_circle_nodes) {
                bad_links.add(findLink(0, node['id']));
            }
        }
        bad_nodes.add(findNode(0));

        bad_nodes = Array.from(bad_nodes);
        bad_links = Array.from(bad_links);
        show_bad_connections = true;
        update();
    }
}
