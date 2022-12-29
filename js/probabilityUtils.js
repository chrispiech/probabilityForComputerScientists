function randInt(a, b) {
	if(b) {
		return randIntHelper(a, b)
	}
	return randIntHelper(0, b)
}

function randIntHelper(min, max){
	min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function logGamma(Z) {
	with (Math) {
		var S=1+76.18009173/Z-86.50532033/(Z+1)+24.01409822/(Z+2)-1.231739516/(Z+3)+.00120858003/(Z+4)-.00000536382/(Z+5);
		var LG= (Z-.5)*log(Z+4.5)-(Z+4.5)+log(S*2.50662827465);
	}
	return LG
}

function betinc(X,A,B) {
	var A0=0;
	var B0=1;
	var A1=1;
	var B1=1;
	var M9=0;
	var A2=0;
	var C9;
	while (Math.abs((A1-A2)/A1)>.00001) {
		A2=A1;
		C9=-(A+M9)*(A+B+M9)*X/(A+2*M9)/(A+2*M9+1);
		A0=A1+C9*A0;
		B0=B1+C9*B0;
		M9=M9+1;
		C9=M9*(B-M9)*X/(A+2*M9-1)/(A+2*M9);
		A1=A0+C9*A1;
		B1=B0+C9*B1;
		A0=A0/B1;
		B0=B0/B1;
		A1=A1/B1;
		B1=1;
	}
	return A1/A
}

function binomialCdf(N,P,X) {
	with (Math) {
		if (N<=0) {
			console.error("sample size must be positive")
		} else if ((P<0)||(P>1)) {
			console.error("probability must be between 0 and 1")
		} else if (X<0) {
			return 0
		} else if (X>=N) {
			return 1
		} else {
			X=floor(X);
			Z=P;
			A=X+1;
			B=N-X;
			S=A+B;
			BT=exp(logGamma(S)-logGamma(B)-logGamma(A)+A*log(Z)+B*log(1-Z));
			if (Z<(A+1)/(S+2)) {
				Betacdf=BT*betinc(Z,A,B)
			} else {
				Betacdf=1-BT*betinc(1-Z,B,A)
			}
			bincdf=1-Betacdf;
		}
		bincdf=round(bincdf*100000)/100000;
	}
    return bincdf;
}

function binomialPmf(N,P,X) {
    return binomialCdf(N,P,X) - binomialCdf(N,P,X-1)
}

function permute(inputArr) {
  var results = [];

  function permuteHelper(arr, memo) {
    var cur, memo = memo || [];

    for (var i = 0; i < arr.length; i++) {
      cur = arr.splice(i, 1);
      if (arr.length === 0) {
        results.push(memo.concat(cur));
      }
      permuteHelper(arr.slice(), memo.concat(cur));
      arr.splice(i, 0, cur[0]);
    }

    return results;
  }

  return permuteHelper(inputArr);
}

function normalize(data) {
	let sum = data.reduce(function(a,b) { return a.concat(b) }) // flatten array
     .reduce(function(a,b) { return a + b });      // sum

    for (var r = 0; r < data.length; r++) {
    	let row = data[r]
    	for (var c = 0; c < row.length; c++) {
    		row[c] = row[c] / sum
    	}
    }
}


/**
 * Draws a bar graph in the given parentDiv (which must be a canvas type)
 */
function drawGraph(charts, parentDivId, data, xLabel = 'x', yLabel='Pr', chartType='bar'){

	if(charts[parentDivId]) {
		charts[parentDivId].destroy()
	}

	var xValues = []
	var yValues = []
	
	for (var i = 0; i < data.length; i++) {
		let datum = data[i]
		xValues.push(datum[0])
		yValues.push(datum[1])
	}

	var config = {
		type: chartType,
		data: {
			labels: xValues,
			datasets: [{
				label: yLabel,
				fill: false,
				backgroundColor: 'blue',
				borderColor: 'blue',
				data: yValues,
				pointRadius:1,
				maxBarThickness:100
			}]
		},
		options: {
			steppedLine: false,
			responsive: true,
			tooltips: {
				mode: 'index',
				intersect: false,
			},
			hover: {
				mode: 'nearest',
				intersect: true
			},
			legend: {
	            display: false
	         },
			scales: {
				xAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: xLabel
					}
				}],
				yAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: yLabel
					},
					ticks: {
                        beginAtZero: true
                    }
				}]
			}
		}
	};
	var ctx = document.getElementById(parentDivId).getContext('2d');
	charts[parentDivId]= new Chart(ctx, config);
}


function drawGrid(charts, parentDivId, matrix, rowVar, colVar) {
	let parentDiv = $("#" + parentDivId)
	var margin = {top: 40, right: 0, bottom: 0, left: 100};

    let rowLabelWidth = 20
    let width = parentDiv.width() - rowLabelWidth;
    let height = width - 70;
    parentDiv.height(parentDiv.width());

var svg = d3.select("#"+parentDivId).append("svg")
    .attr("width", width + margin.left + margin.right + rowLabelWidth )
    .attr("height", height + margin.top + margin.bottom)
    .style("margin-left", -margin.left + "px")
  .append("g")
    .attr("transform", "translate(" + (margin.left+rowLabelWidth) + "," + margin.top + ")");

svg.append("rect")
    .attr("class", "background")
    .attr("width", width)
    .attr("height", height);

var numrows = matrix.length;
var numcols = matrix[0].length;

var x = d3.scale.ordinal()
    .domain(d3.range(numcols))
    .rangeBands([0, width]);

var y = d3.scale.ordinal()
    .domain(d3.range(numrows))
    .rangeBands([0, height]);

var rowLabels = new Array(numrows);
for (var i = 0; i < numrows; i++) {
  rowLabels[i] = i;
}

var columnLabels = new Array(numrows);
for (var i = 0; i < numcols; i++) {
  columnLabels[i] = i;
}

// create a tooltip
  var tooltip = d3.select("#" + parentDivId)
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")
    .style("position", "absolute")

  // Three function that change the tooltip when user hover / move / leave a cell
  var mouseover = function(d) {
  	tooltip
      .style("opacity", 1)
  }
  var mousemove = function(d) {
  	console.log(d)
  	console.log(d3.mouse(this), d3.event.pageX, d3.event.pageY)
    tooltip
      .html(`${d.toFixed(5)}`)
      .style("left", (d3.mouse(this)[0]+100) + "px")
      .style("top", d3.event.pageY + "px")
  }
  var mouseleave = function(d) {
    tooltip.style("opacity", 0)
  }

var colorMap = d3.scale.linear()
    .domain([0, 0.009])
    .range(["white", "blue"]);    
    //.range(["red", "black", "green"]);
    //.range(["brown", "#ddd", "darkgreen"]);

var row = svg.selectAll(".row")
    .data(matrix)
  .enter().append("g")
    .attr("class", "row")
    .attr("transform", function(d, i) { return "translate(0," + y(i) + ")"; });

row.selectAll(".cell")
    .data(function(d) { return d; })
  .enter().append("rect")
    .attr("class", "cell")
    .attr("x", function(d, i) { return x(i); })
    .attr("y", function(d, i) { return y(d); })
    .attr("width", x.rangeBand())
    .attr("height", y.rangeBand())
    .style("stroke-width", 0)
    .on("mouseover", mouseover)
    .on("mousemove", mousemove)
    .on("mouseleave", mouseleave)

row.append("line")
    .attr("x2", width);

row.append("text")
    .attr("x", 0)
    .attr("y", y.rangeBand() / 2)
    .attr("dy", ".32em")
    .attr("text-anchor", "end")
    .text(function(d, i) { return i; });

var column = svg.selectAll(".column")
    .data(columnLabels)
  .enter().append("g")
    .attr("class", "column")
    .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

column.append("line")
    .attr("x1", -width);

column.append("text")
    .attr("x", 6)
    .attr("y", y.rangeBand() / 2)
    .attr("dy", ".32em")
    .attr("text-anchor", "start")
    .text(function(d, i) { return d; });

row.selectAll(".cell")
    .data(function(d, i) { return matrix[i]; })
    .style("fill", colorMap);
}

function drawGridTxt(charts, parentDivId, data) {
	let html = ''
	let headHtml = '<th></th>'
	for (var i = 0; i < data[0].length; i++) {
		let col = i;
		headHtml += `<th>${col}</th>`
	}
	html += `<tr>${headHtml}</tr>`

	for (var r = 0; r < data.length; r++) {
		let rowData = data[r]
		let rowHtml = `<th>${r}</th>`
		for (var c = 0; c < rowData.length; c++) {
			let value = rowData[c]
			rowHtml += `<td>${value.toFixed(5)}</td>`
		}
		html += `<tr>${rowHtml}</tr>`
	}
	$("#"+parentDivId).html(html)
}