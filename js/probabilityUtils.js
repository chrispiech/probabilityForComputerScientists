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