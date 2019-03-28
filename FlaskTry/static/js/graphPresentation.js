function myGraph(el) {
    var id_count = 1;
    var tf_barrier = 100;
    var aua_barrier = 365;
    var mf_barrier = 20;
    var fd_barrier = 12;
    var msp = 0.5;

    // Initialise the graph object
    var graph = this.graph = {
        "nodes":[{"Id":0, "name":"Ego Node", "TF":"", "AUA":"", "CF":[], "MF":[], "FD":[], "Weight":-1, "TSP":-1}],
        "links":[]
    };

    var calc_node_weight = function (TF, AUA){
        var c_TF;
        if (TF > tf_barrier){
            c_TF = 1;
        }else{
            c_TF = TF/tf_barrier;
        }
        var c_AUA;
        if (AUA > aua_barrier){
            c_AUA = 1;
        }else{
            c_AUA = AUA/aua_barrier;
        }

        return (c_TF + c_AUA)/2;
    }

    // Add and remove elements on the graph object
    this.addNode = function (Name, TF, AUA, CF, MF, FD) {
        var node_weight = calc_node_weight(TF, AUA);
        graph["nodes"].push({"Id":id_count, "name":Name, "TF":TF, "AUA":AUA, "CF":CF, "MF":MF, "FD":FD,
                            "Weight":node_weight, "TSP":-1});
    }

    this.removeNode = function (name) {
        graph["nodes"] = _.filter(graph["nodes"], function(node) {return (node["name"] != name)});
        graph["links"] = _.filter(graph["links"], function(link) {return ((link["source"]["name"] != name)&&(link["target"]["name"] != name))});
        update();
    }

    var findNode = function (Id) {
        for (var i in graph["nodes"]) if (graph["nodes"][i]["Id"] === Id) return graph["nodes"][i];
    }

    var findLink = function (source, target){
        for (var i in graph["links"]){
            if (graph["links"][i]["source"]["Id"] === source && graph["links"][i]["target"]["Id"] === target)
                return graph["links"][i];
        }
    }

    var calc_link_weight = function (MF, FD){
        var c_MF;
        if (MF > mf_barrier){
            c_MF = 1;
        }else{
            c_MF = MF/mf_barrier;
        }
        var c_FD;
        if (FD > fd_barrier){
            c_FD = 1;
        }else{
            c_FD = FD/fd_barrier;
        }

        return (c_MF + c_FD)/2;
    }

    var get_first_circle_link_weight = function (source_as_target){
        return findLink(0, source_as_target)['Weight'];
    }

    this.addLink = function (source, i) {
        var target_node = findNode(id_count);
        var link_weight = calc_link_weight(target_node['MF'][i], target_node['FD'][i]);
        var source_node = findNode(source);
        graph["links"].push({"source":source_node,"target":target_node,
                            "MF":target_node['MF'][i], "FD":target_node['FD'][i], "Weight":link_weight});

        if (source > 0){
            first_circle_link_weight = get_first_circle_link_weight(source);
            tsp_to_add = target_node['Weight']*link_weight*source_node['Weight']*first_circle_link_weight;
            if (tsp_to_add > target_node['TSP'])
                target_node['TSP'] = tsp_to_add;
        }
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
        .gravity(0)
        .distance(200)
        .charge(-100)
        .size([w, h]);

    var update = function () {

        var node = vis.selectAll("g.node")
            .data(graph.nodes);

        node.enter().append("g")
            .attr("class", "node")
            .call(force.drag);

        node.append("circle")
            .style("fill", function (d) { if (d.Id ==0){return "#0099ff"}
                                          if (d.CF.includes('0')){return "#00cc00"}
                                          if (d.TSP > 0.5){return "#ff9900"} else{return "#ff0000"}
                                                    })
            .attr("r", 5);

        node.append("text")
            .attr("class", "nodetext")
            .attr("x", "0em")
            .attr("y", 15)
            .text(function(d) { return d.name });

        node.on("mouseover", function(d) {
          var g = d3.select(this); // The node
          // The class is used to remove the additional text later
          var info = g.append('text')
             .classed('info', true)
             .attr('dx', "0em")
             .attr('dy', -10)
             .text(function(d) { if(d.Id ==0){return "id=0"}
                                 else{return "id="+d.Id.toString()+",TF="+d.TF.toString()+",AUA="+d.AUA.toString()}})
             .style("font-size", "12px");
        }).on("mouseout", function() {
              // Remove the info text on mouse out.
              d3.select(this).select('text.info').remove()
            });

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

        var linkText = vis.selectAll("text.link-label").data(graph.links);

        linkText.enter().insert("text")
            .attr("class", "link-label")
        .attr("font-family", "Arial, Helvetica, sans-serif")
        .attr("fill", "Black")
        .style("font", "normal 12px Arial")
        .style("display", "blocked")
        .attr("dy", ".35em")
        .attr("text-anchor", "middle")
        .text(function(d) {
            return "MF="+d["MF"]+",FD="+d["FD"];
        });



        linkText.exit().remove();




        force.on("tick", function() {
          link.attr("x1", function(d) { return d.source.x; })
              .attr("y1", function(d) { return d.source.y; })
              .attr("x2", function(d) { return d.target.x; })
              .attr("y2", function(d) { return d.target.y; });

          linkText
            .attr("x", function(d) {
                return ((d.source.x + d.target.x)/2);
            })
            .attr("y", function(d) {
                return ((d.source.y + d.target.y)/2);
            });

          node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
        });


        // Restart the force layout.
        force
          .nodes(graph.nodes)
          .links(graph.links)
          .start();

//        var q = document.querySelector("[linkTextTitle]");
//        if (q){
//            q.addEventListener("mouseover", function( event ) {
//                // highlight the mouseover target
//                event.target.style.color = "orange";
//
//            })
//        }
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

    graph.addNode(name, tf, aua, cf, mf, fd);
    var i;
    for (i = 0; i < cf.length; i++) {
        graph.addLink(parseInt(cf[i]), i);
    }
    graph.increase_id_count();
}