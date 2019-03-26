function myGraph(el) {
    var id_count = 1;

    // Initialise the graph object
    var graph = this.graph = {
        "nodes":[{"Id":0, "name":"Ego Node", "TF":"", "AUA":"", "CF":[], "MF":[], "FD":[]}],
        "links":[]
    };

    // Add and remove elements on the graph object
    this.addNode = function (Name, TF, AUA, CF, MF, FD) {
        graph["nodes"].push({"Id":id_count, "name":Name, "TF":TF, "AUA":AUA, "CF":CF, "MF":MF, "FD":FD});
    }

    this.removeNode = function (name) {
        graph["nodes"] = _.filter(graph["nodes"], function(node) {return (node["name"] != name)});
        graph["links"] = _.filter(graph["links"], function(link) {return ((link["source"]["name"] != name)&&(link["target"]["name"] != name))});
        update();
    }

    var findNode = function (Id) {
        for (var i in graph["nodes"]) if (graph["nodes"][i]["Id"] === Id) return graph["nodes"][i];
    }

    this.addLink = function (source) {
        graph["links"].push({"source":source,"target":id_count});
        update();
    }

    this.increase_id_count = function () {
        id_count++;
    }

    // set up the D3 visualisation in the specified element
    var w = $(el).innerWidth(),
        h = $(el).innerHeight();

    var vis = d3.select(el).append("svg:svg")
        .attr("width", w)
        .attr("height", h);

    var force = d3.layout.force()
        .nodes(graph.nodes)
        .links(graph.links)
        .gravity(.05)
        .distance(100)
        .charge(-100)
        .size([w, h]);

    var update = function () {

        var node = vis.selectAll("g.node")
            .data(graph.nodes);

        node.enter().append("g")
            .attr("class", "node")
            .call(force.drag);

        node.append("circle")
            .attr("r", 5);;

        node.append("text")
            .attr("class", "nodetext")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(function(d) { return d.name });

        node.exit().remove();


        var link = vis.selectAll("line.link")
            .data(graph.links);

        link.enter().insert("line")
            .attr("class", "link")
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        link.exit().remove();



        force.on("tick", function() {
          link.attr("x1", function(d) { return d.source.x; })
              .attr("y1", function(d) { return d.source.y; })
              .attr("x2", function(d) { return d.target.x; })
              .attr("y2", function(d) { return d.target.y; });

          node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
        });

        // Restart the force layout.
        force
          .nodes(graph.nodes)
          .links(graph.links)
          .start();
    }

    // Make it all go
    update();
}


graph = new myGraph("#my_dataviz");

// These are the sort of commands I want to be able to give the object.
function addNode() {
    var name = document.getElementById("NodeName").value
    var tf = document.getElementById("TF").value
    var aua = document.getElementById("AUA").value
    var cf = document.getElementById("CF").value.split(",")
    var mf = document.getElementById("MF").value.split(",")
    var fd = document.getElementById("FD").value.split(",")

    console.log(cf.length);
    graph.addNode(name, tf, aua, cf, mf, fd);
    var i;
    for (i = 0; i < cf.length; i++) {
        console.log('a');
        graph.addLink(parseInt(cf[i]));
    }
    graph.increase_id_count();
}