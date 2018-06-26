var svgWidth = 960;
var svgHeight = 500;

var margin = {
  top: 20,
  right: 40,
  bottom: 100,
  left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
var svg = d3.select(".chart")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight)

var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

  var obesityLabel=chartGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left + 20)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .attr("class", "axisText")
    .text("Obese (%)");
  
  // var smokeLabel=chartGroup.append("text")
  //   .attr("transform", "rotate(-90)")
  //   .attr("y", 0 - margin.left + 40)
  //   .attr("x", 0 - (height / 2))
  //   .attr("dy", "1em")
  //   .attr("class", "axisText")
  //   .text("Smokes (%)");

  // var healthLabel=chartGroup.append("text")
  //   .attr("transform", "rotate(-90)")
  //   .attr("y", 0 - margin.left + 60)
  //   .attr("x", 0 - (height / 2))
  //   .attr("dy", "1em")
  //   .attr("class", "axisText")
  //   .text("Lacks Healthcare (%)");

    var povertyLabel=chartGroup.append("text")
    .attr("transform", `translate(${width/2}, ${height + margin.top + 30})`)
    .attr("class", "axisText")
    .text("Poverty (%)");

  // var ageLabel=chartGroup.append("text")
  //   .attr("transform", `translate(${width/2}, ${height + margin.top + 50})`)
  //   .attr("class", "axisText")
  //   .text("Age (Median)");

  // var incomeLabel=chartGroup.append("text")
  //   .attr("transform", `translate(${width/2}, ${height + margin.top + 70})`)
  //   .attr("class", "axisText")
  //   .text("Household Income (Median)");

// Import Data
d3.csv("data.csv", function (err, data) {
  if (err) throw err;
  
  // Step 1: Parse Data/Cast as numbers
   // ==============================
  data.forEach(function (data) {
    data.poverty = +data.poverty;
    data.obesity = +data.obesity;
    
  });

  // Step 2: Create scale functions
  // ==============================
  var xLinearScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.poverty)])
    .range([0, width]);

  var yLinearScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.obesity)])
    .range([height, 0]);

  // Step 3: Create axis functions
  // ==============================
  var bottomAxis = d3.axisBottom(xLinearScale);
  var leftAxis = d3.axisLeft(yLinearScale);

  // Step 4: Append Axes to the chart
  // ==============================
  chartGroup.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(bottomAxis);

  chartGroup.append("g")
    .call(leftAxis);

   // Step 5: Create Circles
  // ==============================
  var circlesGroup = chartGroup.selectAll("circle")
  .data(data)
  .enter()
  .append("circle")
  .attr("cx", d => xLinearScale(d.poverty))
  .attr("cy", d => yLinearScale(d.obesity))
  .attr("r", "15")
  .attr("fill", "purple")
  .attr("opacity", ".5");

  // Add labels
  var labelsGroup = chartGroup.selectAll("circleText")
  .data(data)
  .enter()
  .append("text")
  .attr("x",d => xLinearScale(d.poverty)-12)
  .attr("y",d => yLinearScale(d.obesity)+5)
  .style('fill','white')
  .text(d => `${d.abbr}`);
  

  // Step 6: Initialize tool tip
  // ==============================
  var toolTip = d3.tip()
    .attr("class", "tooltip")
    .offset([80, -60])
    .html(d =>
      `${d.abbr}<br>%Poverty: ${d.poverty}<br>%Obesity: ${d.obesity}`
    );

  // Step 7: Create tooltip in the chart
  // ==============================
  chartGroup.call(toolTip);

  // Step 8: Create event listeners to display and hide the tooltip
  // ==============================
  circlesGroup.on("mouseover", function (data) {
      toolTip.show(data);
    })
    // onmouseout event
    .on("mouseout", function (data, index) {
      toolTip.hide(data);
    });

  
});

