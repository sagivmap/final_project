function myGraph(el) {

    // Initialise the graph object
    var graph = this.graph = {
        "nodes":[{"name":"Cause"},{"name":"Effect"}],
        "links":[{"source":0,"target":1}]
    };

    // Add and remove elements on the graph object
    this.addNode = function (name) {
        graph["nodes"].push({"name":name});
        update();
    }

    this.removeNode = function (name) {
        graph["nodes"] = _.filter(graph["nodes"], function(node) {return (node["name"] != name)});
        graph["links"] = _.filter(graph["links"], function(link) {return ((link["source"]["name"] != name)&&(link["target"]["name"] != name))});
        update();
    }

    var findNode = function (name) {
        for (var i in graph["nodes"]) if (graph["nodes"][i]["name"] === name) return graph["nodes"][i];
    }

    this.addLink = function (source, target) {
        graph["links"].push({"source":findNode(source),"target":findNode(target)});
        update();
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

        var link = vis.selectAll("line.link")
            .data(graph.links);

        link.enter().insert("line")
            .attr("class", "link")
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        link.exit().remove();

        var node = vis.selectAll("g.node")
            .data(graph.nodes);

        node.enter().append("g")
            .attr("class", "node")
            .call(force.drag);

        node.append("image")
            .attr("class", "circle")
            .attr("xlink:href", "https://d3nwyuy0nl342s.cloudfront.net/images/icons/public.png")
            .attr("x", "-8px")
            .attr("y", "-8px")
            .attr("width", "16px")
            .attr("height", "16px");

        node.append("text")
            .attr("class", "nodetext")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(function(d) { return d.name });

        node.exit().remove();

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
graph.addNode("A");
graph.addNode("B");
graph.addLink("A", "B");
graph.addNode("Alexxxx");