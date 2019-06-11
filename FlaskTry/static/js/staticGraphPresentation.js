
$.getJSON("static/file.json", function(json) {

    nodes = json.nodes;
    links = json.links;

    var width = $("#my_dataviz").innerWidth(),
        height = $("#my_dataviz").innerHeight(),
        id_count = 1,
        tf_barrier = 100,
        aua_barrier = 365,
        mf_barrier = 20,
        fd_barrier = 12,
        msp = 0.5,
        r = 5,
        links = links,
        nodes = nodes,
        getXloc = d3.scalePoint().domain([0, 1, 2]).range([100, width - 100]);

    var zoom = d3.select(".everything");

    var zoom_handler = d3.zoom()
    .on("zoom", zoom_actions);
    zoom_handler(zoom);
    function zoom_actions(){
        zoom.attr("transform", d3.event.transform)
    }

    var simulation = d3.forceSimulation(nodes)
        .force('x', d3.forceX((d) => getXloc(d.level)).strength(4))
        .force('collide', d3.forceCollide(r * 4))
        .force('charge', d3.forceManyBody().strength(0))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('link', d3.forceLink().links(links).id(function (d) {
            return d.id
        }))
        .on('tick', ticked);

    var graphOptionsElements = document.getElementById('graphOptions');
    graphOptionsElements.addEventListener('change', function () {
        if (this.value === "IFM") {
            changeToIFM();
        } else if (this.value === "CB") {
            changeToCB();
        }
    }, false);

    function changeToIFM() {
    document.getElementById("svg-id").removeAttribute("viewBox");
    simulation = d3.forceSimulation(nodes)
        .force('x', d3.forceX((d) => getXloc(d.level)).strength(4))
        .force('collide', d3.forceCollide(r * 4))
        .force('charge', d3.forceManyBody().strength(0))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('link', d3.forceLink().links(links).id(function (d) { return d.id }))
        .on('tick', ticked);

    update();
}

function changeToCB() {

    document.getElementById("svg-id").setAttribute("viewBox", -1 * width / 2 + " " + -1 * height / 2 + " " + width + " " + height);
    simulation = d3.forceSimulation(nodes)
        .force("r", d3.forceRadial(function (d) { return d.level * 200; }).strength(1))
        .force('collide', d3.forceCollide(r * 4))
        .force('link', d3.forceLink().links(links).id(function (d) { return d.id }).strength(0.1))
        .on("tick", ticked);

    update();

}



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


    function update() {

        var link = d3.select('.links')
            .selectAll('line.link')
            .data(links).enter().insert("line")
            .attr("class", "link")
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        link.exit().remove();

        var node = d3.select('.nodes')
            .selectAll('g.node')
            .data(nodes).enter().append("g")
            .attr("class", "node");

        node.append("circle")
            .style("fill", function (d) {
                if (d.id == 0 || d.id == "Ego_Node") {
                    return "#0099ff"
                }
                if (d.level == 1) {
                    return "#00cc00"
                }
                if (d.TSP > 0.5) {
                    return "#ff9900"
                } else {
                    return "#ff0000"
                }
            })
            .attr("r", r);

        node.append("text")
            .attr("class", "nodetext")
            .attr("x", "0em")
            .attr("y", 15)
            .text(function (d) {
                return d.Name
            });

        node.on("mouseover", function (d) {
            /*
            var g = d3.select(this); // The node
            // The class is used to remove the additional text later
            var info = g.append('text')
                .classed('info', true)
                .attr('dx', "0em")
                .attr('dy', -10)
                .text(function (d) {
                    if (d.id == 0 || d.id == "Ego_Node") {
                        return "id=0"
                    }
                    else {
                        return "id=" + d.id.toString() + ",TF=" + d.TF.toString() + ",AUA=" + d.AUA.toString()
                    }
                })
                .style("font-size", "12px");
            */
            document.getElementById("idForId").innerHTML = d.id;
            document.getElementById("idForName").innerHTML = d.Name;
            document.getElementById("idForTF").innerHTML = d.TF;
            document.getElementById("idForAUA").innerHTML = d.AUA;
            document.getElementById("idForMF").innerHTML = d.MF;
            document.getElementById("idForTSP").innerHTML = d.TSP;
            document.getElementById("idForlevel").innerHTML = d.level;


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
        simulation.nodes(nodes);
        simulation.force("link").links(links).id(function (d) {
            return d.id
        });
        simulation.on('tick', ticked)
        simulation.alpha(1).restart();
    }

    function ticked() {
        var link = d3.select('.links')
            .selectAll('line.link')
            .data(links);
        link.attr("x1", function (d) {
            return d.source.x;
        })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });


        var node = d3.select('.nodes')
            .selectAll('g.node')
            .data(nodes);



        node.attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    }


    update();

});