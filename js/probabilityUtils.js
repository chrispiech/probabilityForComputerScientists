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


function drawGraph(charts, parentDivId, data, xLabel = 'x', yLabel='Pr'){

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
		type: 'bar',
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