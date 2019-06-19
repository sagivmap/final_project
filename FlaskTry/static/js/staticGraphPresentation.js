if (document.getElementById("linkToCSVfile").getAttribute("href") === "/database_download/")
    document.getElementById("linkToCSVfileButton").style.display = "none";
else
    document.getElementById("linkToCSVfileButton").style.display = "block";

var nodes,
    links,
    SummaryGraph = false,
    msp = 0.5;

function get_all_low_tsp_second_level_nodes() {
    var nodes_to_return = [];
    for (var i in nodes) {
        if (nodes[i]["level"] === 2 && nodes[i]["TSP"] < msp) {
            var node_to_add = {
                "id": nodes[i]["id"],
                "name": nodes[i]["Name"],
                "TF": parseInt(nodes[i]["TF"],10),
                "AUA": parseInt(nodes[i]["AUA"],10),
                "CF": nodes[i]["CF"],
                "MF": parseInt(nodes[i]["MF"],10),
                "FD": parseInt(nodes[i]["FD"],10),
                "Weight": nodes[i]["Weight"],
                "TSP": parseFloat(nodes[i]["TSP"]),
                "level": nodes[i]["level"]
            }
            nodes_to_return.push(node_to_add);
        }
    }
    return nodes_to_return;
}

function get_all_high_tsp_second_level_nodes() {
    var nodes_to_return = [];
    for (var i in nodes) {
        if (nodes[i]["level"] === 2 && nodes[i]["TSP"] >= msp) {
            var node_to_add = {
                "id": nodes[i]["id"],
                "name": nodes[i]["Name"],
                "TF": parseInt(nodes[i]["TF"], 10),
                "AUA": parseInt(nodes[i]["AUA"], 10),
                "CF": nodes[i]["CF"],
                "MF": parseInt(nodes[i]["MF"], 10),
                "FD": parseInt(nodes[i]["FD"], 10),
                "Weight": nodes[i]["Weight"],
                "TSP": parseFloat(nodes[i]["TSP"]),
                "level": nodes[i]["level"]
            }
            nodes_to_return.push(node_to_add);
        }
    }
    return nodes_to_return;
}

function get_all_first_level_nodes() {
    var nodes_to_return = [];
    for (var i in nodes) {
        if (nodes[i]["level"] === 1) {
            var node_to_add = {
                "id": nodes[i]["id"],
                "name": nodes[i]["Name"],
                "TF": parseInt(nodes[i]["TF"],10),
                "AUA": parseInt(nodes[i]["AUA"],10),
                "CF": nodes[i]["CF"],
                "MF": parseInt(nodes[i]["MF"],10),
                "FD": parseInt(nodes[i]["FD"],10),
                "Weight": nodes[i]["Weight"],
                "TSP": parseFloat(nodes[i]["TSP"]),
                "level": nodes[i]["level"]
            }
            nodes_to_return.push(node_to_add);
        }
    }
    return nodes_to_return;
}

function get_mf_fd_avarage(mffd) {
    var summ = 0;
    for (var i in mffd) {
        summ += mffd[i];
    }
    console
    return summ / mffd.length;
}

function getAvgOfCircles(circle, bad) {
    var circlesToCalc;
    if (circle === 1) {
        circlesToCalc = get_all_first_level_nodes();
    } else if (circle === 2) {
        if (bad) {
            circlesToCalc = get_all_low_tsp_second_level_nodes();
        } else {
            circlesToCalc = get_all_high_tsp_second_level_nodes();
        }
    }

    tf_count = circlesToCalc.length
    aua_count = circlesToCalc.length
    mf_count = circlesToCalc.length
    fd_count = circlesToCalc.length
    tsp_count = circlesToCalc.length

    var tf_sum = 0,
        aua_sum = 0,
        mf_sum = 0,
        fd_sum = 0,
        tsp_sum = 0;

    for (var i in circlesToCalc) {
        if (circlesToCalc[i]["TF"] === -1) {
            tf_count--;
        } else {
            tf_sum += circlesToCalc[i]["TF"]
        } if (circlesToCalc[i]["AUA"] === -1) {
            aua_count--;
        } else {
            aua_sum += circlesToCalc[i]["AUA"]
        }
        if (Array.isArray(circlesToCalc[i]["MF"])) {
            if (get_mf_fd_avarage(circlesToCalc[i]["MF"]) === -1) {
                mf_count--;
            } else {
                mf_sum += get_mf_fd_avarage(circlesToCalc[i]["MF"])
            }
        } else {
            if (circlesToCalc[i]["MF"] === -1) {
                mf_count--;
            } else {
                mf_sum += circlesToCalc[i]["MF"]
            }
        }
        if (Array.isArray(circlesToCalc[i]["FD"])) {
            if (get_mf_fd_avarage(circlesToCalc[i]["FD"]) === -1) {
                fd_count--;
            } else {
                fd_count += get_mf_fd_avarage(circlesToCalc[i]["FD"])
            }
        } else if (typeof circlesToCalc[i]["FD"] !== 'undefined') {
            if (circlesToCalc[i]["FD"] === -1) {
                fd_count--;
            } else {
                fd_count += circlesToCalc[i]["FD"]
            }
        }
        if (circlesToCalc[i]["TSP"] === -1) {
            tsp_count--;
        } else {
            tsp_sum += circlesToCalc[i]["TSP"]
        }
    }
    console.log(tf_sum)
    console.log(tf_count)
    if (circle === 2)
        return [tf_sum / tf_count, aua_sum / aua_count, mf_sum / mf_count, fd_sum / fd_count, circlesToCalc.length, tsp_sum / tsp_count]
    else if (circle === 1)
        return [tf_sum / tf_count, aua_sum / aua_count, mf_sum / mf_count, fd_sum / fd_count, circlesToCalc.length]
}

$.getJSON("static/file.json", function (json) {

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
        } else if (this.value === "Summ") {
            changeToSumm();
        }
    }, false);



    var summaryNodes = [{ "id": 0, "name": "Ego Node", "TF": "", "AUA": "", "CF": [], "MF": [], "FD": [], "Weight": -1, "TSP": -1, "level": 0 }];
    var summaryLinks = []

    function changeToSumm() {
        summaryNodes = [{ "id": 0, "name": "Ego Node", "TF": "", "AUA": "", "CF": [], "MF": [], "FD": [], "Weight": -1, "TSP": -1, "level": 0 }];
        summaryLinks = []
        SummaryGraph = true;
        document.getElementById("myForm").style.display = "none";
        document.getElementById("svg-id").removeAttribute("viewBox");
        
        first_circle_avg = getAvgOfCircles(1, true);
        second_bad_circle_avg = getAvgOfCircles(2, true);
        second_good_circle_avg = getAvgOfCircles(2, false);

        if (first_circle_avg[4] > 0) {
            summaryNodes.push({ "id": 1, "name": "#1 Circles Avarage", "TF": first_circle_avg[0], "AUA": first_circle_avg[1], "MF": first_circle_avg[2], "FD": first_circle_avg[3], "TSP": -1, "size": first_circle_avg[4], "level": 1 })
            summaryLinks.push({ "source": 0, "target": 1 });
            if (second_bad_circle_avg[4] > 0) {
                summaryNodes.push({ "id": 2, "name": "#2 Bad Circles Avarage", "TF": second_bad_circle_avg[0], "AUA": second_bad_circle_avg[1], "MF": second_bad_circle_avg[2], "FD": second_bad_circle_avg[3], "TSP": second_bad_circle_avg[5], "size": second_bad_circle_avg[4], "level": 2 })
                summaryLinks.push({ "source": 1, "target": 2 });
            }
            if (second_good_circle_avg[4] > 0) {
                summaryNodes.push({ "id": 3, "name": "#2 Good Circles Avarage", "TF": second_good_circle_avg[0], "AUA": second_good_circle_avg[1], "MF": second_good_circle_avg[2], "FD": second_good_circle_avg[3], "TSP": second_good_circle_avg[5], "size": second_good_circle_avg[4], "level": 2 })
                summaryLinks.push({ "source": 1, "target": 3 });
            }
        }

        console.log(summaryNodes);
        console.log(summaryLinks);

        simulation = d3.forceSimulation(summaryNodes)
            .force('x', d3.forceX((d) => getXloc(d.level)).strength(4))
            .force('collide', d3.forceCollide(r * 21))
            .force('charge', d3.forceManyBody().strength(0))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('link', d3.forceLink().links(summaryLinks).id(function (d) { return d.id }))
            .on('tick', ticked);

        d3.select('.links').selectAll('line.link').remove();
        d3.select('.nodes').selectAll('g.node').remove();

        update();
    }

    function changeToIFM() {
        SummaryGraph = false;
        document.getElementById("myForm").style.display = "block";
        document.getElementById("svg-id").removeAttribute("viewBox");
        simulation = d3.forceSimulation(nodes)
            .force('x', d3.forceX((d) => getXloc(d.level)).strength(4))
            .force('collide', d3.forceCollide(r * 4))
            .force('charge', d3.forceManyBody().strength(0))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('link', d3.forceLink().links(links).id(function (d) { return d.id }))
            .on('tick', ticked);
        d3.select('.links').selectAll('line.link').remove();
        d3.select('.nodes').selectAll('g.node').remove();
        update();
    }

    function changeToCB() {
        SummaryGraph = false;
        document.getElementById("myForm").style.display = "block";
        document.getElementById("svg-id").setAttribute("viewBox", -1 * width / 2 + " " + -1 * height / 2 + " " + width + " " + height);
        simulation = d3.forceSimulation(nodes)
            .force("r", d3.forceRadial(function (d) { return d.level * 200; }).strength(1))
            .force('collide', d3.forceCollide(r * 4))
            .force('link', d3.forceLink().links(links).id(function (d) { return d.id }).strength(0.1))
            .on("tick", ticked);
        d3.select('.links').selectAll('line.link').remove();
        d3.select('.nodes').selectAll('g.node').remove();
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
            .data(SummaryGraph ? summaryLinks : links).enter().insert("line")
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
            .data(SummaryGraph ? summaryNodes : nodes)
        node_enter = node.enter().append("g")
            .attr("class", "node");

        if (SummaryGraph) {

            node_enter.append("rect").style("fill", function (d) {
                if (d.id == 0) { return "#0099ff" }
                if (d.id == 1) { return "#00cc00" }
                if (d.id == 3) { return "#ff9900" } else { return "#ff0000" }
            })
                .attr("width", function (d) {
                    if (d.id == 0) { return 50 }
                    if (d.id == 1) { return 200 }
                    if (d.id == 3) { return 200 } else { return 200 }
                })
                .attr("height", function (d) {
                    if (d.id == 0) { return 50 }
                    if (d.id == 1) { return 210 }
                    if (d.id == 3) { return 210 } else { return 210 }
                })
                .attr("x", function (d) {
                    if (d.id == 0) { return -25 }
                    if (d.id == 1) { return -105 }
                    if (d.id == 3) { return -105 } else { return -105 }
                })
                .attr("y", function (d) {
                    if (d.id == 0) { return -25 }
                    if (d.id == 1) { return -105 }
                    if (d.id == 3) { return -105 } else { return -105 }
                }).attr('ry', 20)
                .attr('rx', 20)
                .style('stroke', 'black')
                .style('stroke-width', 5);

            node_enter.append('text').text(function (d) {
                if (d.id == 0) { return "Ego Node" }
                else { return d.name + "," }

            }).style("white-space", "pre-line").style('color', 'black').style("opacity", 1).style('fill', 'black').style('font-size', '12px')
                .attr('y', function (d) {
                    if (d.id == 0) { return 0 }
                    else { return -50 }
                })
            node_enter.append('text').text(function (d) {
                if (d.id == 0) { return "" }
                else { return "size: " + d.size + "," }

            }).style("white-space", "pre-line").style('color', 'black').style("opacity", 1).style('fill', 'black').style('font-size', '12px')
                .attr('y', function (d) {
                    if (d.id == 0) { return 0 }
                    else { return -35 }
                })
            node_enter.append('text').text(function (d) {
                if (d.id == 0) { return "" }
                else { return "avg TF: " + d.TF + "," }
            }).style("white-space", "pre-line").style('color', 'black').style("opacity", 1).style('fill', 'black').style('font-size', '12px')
                .attr('y', function (d) {
                    if (d.id == 0) { return 0 }
                    else { return -20 }
                })
            node_enter.append('text').text(function (d) {
                if (d.id == 0) { return "" }
                else { return "avg AUA: " + d.AUA + "," }
            }).style("white-space", "pre-line").style('color', 'black').style("opacity", 1).style('fill', 'black').style('font-size', '12px')
                .attr('y', function (d) {
                    if (d.id == 0) { return 0 }
                    else { return -5 }
                })
            node_enter.append('text').text(function (d) {
                if (d.id == 0) { return "" }
                else { return "avg MF: " + d.MF + "," }
            }).style("white-space", "pre-line").style('color', 'black').style("opacity", 1).style('fill', 'black').style('font-size', '12px')
                .attr('y', function (d) {
                    if (d.id == 0) { return 0 }
                    else { return 10 }
                })
            node_enter.append('text').text(function (d) {
                if (d.id == 0) { return "" }
                else { return "avg FD: " + d.FD + "," }
            }).style("white-space", "pre-line").style('color', 'black').style("opacity", 1).style('fill', 'black').style('font-size', '12px')
                .attr('y', 25)

            node_enter.append('text').text(function (d) {
                if (d.id == 0) { return "" }
                if (d.id == 1) { return "" }
                else { return "avg TSP: " + d.TSP }
            }).style("white-space", "pre-line").style('color', 'black').style("opacity", 1).style('fill', 'black').style('font-size', '12px')
                .attr('y', function (d) {
                    if (d.id == 0) { return 0 }
                    else { return 40 }
                })

        } else {

            node_enter.append("circle")
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

            node_enter.append("text")
                .attr("class", "nodetext")
                .attr("x", "0em")
                .attr("y", 15)
                .text(function (d) {
                    return d.Name
                });
        }

        if (!SummaryGraph) {

            node_enter.on("mouseover", function (d) {

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
        } else {
            node_enter.on("mouseover", function (d) {
                d3.selectAll('line.link')
                    .filter(function (l) {
                        return (d.id != 0 && (d.id == l.source.id || d.id == l.target.id));
                    })
                    .style("opacity", 1)

            }).on("mouseout", function () {
                d3.selectAll('line.link').style("opacity", 0.1)
            });
        }

        node_enter.exit().remove();

        drag_handler(node_enter);
        simulation.nodes(SummaryGraph ? summaryNodes : nodes);
        simulation.force("link").links(SummaryGraph ? summaryLinks : links).id(function (d) {
            return d.id
        });
        simulation.on('tick', ticked)
        simulation.alpha(1).restart();
    }

    function ticked() {
        var link = d3.select('.links')
            .selectAll('line.link')
            .data(SummaryGraph ? summaryLinks : links);
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
            .data(SummaryGraph ? summaryNodes : nodes);



        node.attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    }


    update();

});