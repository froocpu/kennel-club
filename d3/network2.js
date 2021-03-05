async function networkChart() {

    const data = await d3.json("./dogs.json")
    // console.log(data)

    const height = 750
    const width = 1500

    const links = data.links.map(d => Object.create(d));
    const nodes = data.nodes.map(d => Object.create(d));
  
  const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(0).strength(1))
      .force("charge", d3.forceManyBody().strength(-50))
      .force("x", d3.forceX())
      .force("y", d3.forceY());
  
    const svg = d3.select("#svg")
        .append("svg")
        .attr("viewBox", [-width / 2, -height / 2, width, height])
   
    const link = svg.append("g")
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke", function(d){
            if (d.value == "damed") {return "#FFB6C1"}
            else if (d.value == "sired") {return "#0000A0"}
            else {return "#7C7C7E"};
        })
        .attr("stroke-width", 0.7)
        .attr("stroke-opacity", 0.5);

    // Define the div for the tooltip
    var div = d3.select("body").append("div")	
        .attr("class", "tooltip")				
        .style("opacity", 1)
        .style("display", 'inline')
        .style("color", "#7C7C7E")
        .style("font-size","10px");

    const node = svg.append("g")
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", 3)
        .attr("fill", function(d){
            if (d.colour == "BLACK") {return "#000000"}
            else if (d.colour == "YELLOW") {return "#f2d974"}
            else if (d.colour == "BROWN") {return "#964B00"}
            else {return "#7C7C7E"}
        })
        .attr("fill-opacity", 0.7)
        .on("mouseover", function(event, d){
            console.log(d);
            div.transition()
            .duration(200)
            .style("opacity", 1);
            div.html(d.label)
            .style("left", (event.pageX) + "px")
            .style("top", (event.pageY - 28) + "px");

        })
        .on("mouseout", function(d){
          div.transition()
          .duration(500)
          .style("opacity", 0);
        });
        
    node.append("title")
        .text(d => d.label);

    simulation.on("tick", () => {
      link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);
  
      node
          .attr("cx", d => d.x)
          .attr("cy", d => d.y)
    });

  }
  networkChart()
