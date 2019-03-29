var graph = {
  "nodes": [
    {"id": "Ego_Node", "Name": "Ego_Node", "TF": "0", "MF": "0", "AUA": "0","x": 100, "y": 100, "TSP": -1},
    {"id": "bob", "Name": "bob", "TF": "89", "MF": "6", "AUA": "197", "x": 300, "y": 300, "TSP": -1},
    {"id": "charlie", "Name": "charlie", "TF": "78", "MF": "9", "AUA": "124", "x": 340, "y": 340, "TSP": -1},
    {"id": "david", "Name": "david", "TF": "97", "MF": "21", "AUA": "356", "x": 360, "y": 360, "TSP": -1},
    {"id": "eve", "Name": "eve", "TF": "76", "MF": "3", "AUA": "51", "TSP": "0.17" , "x": 620, "y": 620},
    {"id": "frank", "Name": "frank", "TF": "95", "MF": "2", "AUA": "334", "TSP": "0.32" ,"x": 660, "y": 660},
  ],
  "links": [
      {"source": 1, "target": 4},
      {"source": 3, "target": 5},
      {"source": 0, "target": 3},
      {"source": 0, "target": 1},
      {"source": 3, "target": 4},
      {"source": 2, "target": 4},
      {"source": 2, "target": 5},
      {"source": 0, "target": 2},
  ]
}

var width = 900,
    height = 500;

var force = d3.layout.force()
    .size([width, height])
    .charge(-100)
    .linkDistance(200)
    .on("tick", tick);

var drag = force.drag()
    .on("dragstart", dragstart)
    .on("dragend", dragend);

var svg = d3.select("#my_dataviz").append("svg")
    .attr("width", width)
    .attr("height", height);

var link = svg.selectAll(".link"),
    node = svg.selectAll(".node");

  force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();

  link = link.data(graph.links)
    .enter().append("line")
      .attr("class", "link");

  node = node.data(graph.nodes)
    .enter().append("g").attr("class","node");



      node.append("text")
            .attr("class", "nodetext")
            .attr("x", "0em")
            .attr("y", 15)
            .text(function(d) { return d.Name });

      node.append("circle")
      .attr("class", "node")
      .style("fill", function (d) { if (d.id =='Ego_Node'){return "#0099ff"}
                                          if (d.TSP == -1){return "#00cc00"}
                                          if (d.TSP > 0.3){return "#ff9900"} else{return "#ff0000"}
                                                    })
      .attr("r", 12)
      .call(drag);

      node.on("mouseover", function(d) {
          var g = d3.select(this); // The node
          // The class is used to remove the additional text later
          var info = g.append('text')
             .classed('info', true)
             .attr('dx', "0em")
             .attr('dy', -10)
             .text(function(d) { if(d.id =="Ego_Node"){return "id=0"}
                                 else{return "id="+d.id+",TF="+d.TF+",AUA="+d.AUA}})
             .style("font-size", "12px");
        }).on("mouseout", function() {
              // Remove the info text on mouse out.
              d3.select(this).select('text.info').remove()
            });


function tick() {
  link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  // node.attr("cx", function(d) { return d.x; })
  //     .attr("cy", function(d) { return d.y; });

  node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
}

function dragstart(d) {
    // d.fixed = true;
    // d3.select(this).classed("fixed", true);
d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragend(d) {
    // var self = this;
    // setTimeout(function() {
    //     d.fixed = false;
    //     d3.select(self).classed("fixed", false);
    // }, 2000);
    d.fx = d3.event.x;
  d.fy = d3.event.y;
}




































// var width = 960,
//     height = 500
//
// var svg = d3.select("#my_dataviz").append("svg")
//     .attr("width", width)
//     .attr("height", height);
//
// // var force = d3.layout.force()
// //     .gravity(.05)
// //     .distance(100)
// //     .charge(-100)
// //     .size([width, height]);
//
// var force = d3.layout.force()
//     .size([width, height])
//     .charge(-400)
//     .linkDistance(40)
//     .on("tick", tick);
//
// function dragstart(d) {
//     d.fixed = true;
//     d3.select(this).classed("fixed", true);
// }
//
// function dragend(d) {
//     var self = this;
//     setTimeout(function() {
//         d.fixed = false;
//         d3.select(self).classed("fixed", false);
//     }, 2000);
// }
//
//
// var drag = force.drag()
//     .on("dragstart", dragstart)
//     .on("dragend", dragend);
//
// d3.json("static/file.json", function(json) {
//   force
//       .nodes(json.nodes)
//       .links(json.links)
//       .start();
//
//   var link = svg.selectAll(".link")
//       .data(json.links)
//     .enter().append("line")
//       .attr("class", "link");
//
//   var node = svg.selectAll(".node")
//       .data(json.nodes)
//     .enter().append("g")
//       .attr("class", "node")
//       .call(drag);
//
//   node.append("circle")
//       .attr("r","5");
//
//   node.append("text")
//       .attr("dx", 12)
//       .attr("dy", ".35em")
//       .text(function(d) { return d.Name });
//
//   force.on("tick", function() {
//      link.attr("x1", function(d) { return d.source.x; })
//       .attr("y1", function(d) { return d.source.y; })
//       .attr("x2", function(d) { return d.target.x; })
//       .attr("y2", function(d) { return d.target.y; });
//
//     node.attr("cx", function(d) { return d.x; })
//         .attr("cy", function(d) { return d.y; });
//   });
//
// });
