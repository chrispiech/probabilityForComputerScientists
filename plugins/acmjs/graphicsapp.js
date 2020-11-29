/***** AVAILABLE JAVASCRIPT FUNCTIONS ******/


/* Function: GraphicsApp()
 * --------------------------------
 * Creates a new GraphicsApp object and returns it.
 *
 * Parameters: none
 */
function GraphicsApp() {}




/* Function: addButton(buttonName)
 * -----------------------------------------------
 * Creates and adds a new button to the top area of the webpage.  The button
 * will display the text buttonName.
 *
 * Parameters:
 * -----------
 *	buttonName: the text that is displayed on the button.
 */
GraphicsApp.prototype.addButton = function(buttonName, callbackFn) {
	var inputDiv = document.getElementById("inputDiv");
	var button = document.createElement("BUTTON");
	button.textContent = buttonName;

	button.onclick = callbackFn;

    if (typeof(inputDiv) === "undefined") {
        inputDiv = document.getElementsByTagName('body');   
    }
	inputDiv.appendChild(button);
}



/* Function: addTextField()
 * -----------------------------
 * Creates and adds a new text field to the top area of the webpage.
 * Returns the text field object that was added to the page.
 *
 * Parameters: none
 * Returns: the text field that was created.
 */
GraphicsApp.prototype.addTextField = function() {

	// Make a new text field
	var textField = document.createElement("INPUT");
	textField.type = "text";
	textField.id = "inputField";

	// Append it inside our input div
	var inputDiv = document.getElementById("inputDiv");

	if (typeof(inputDiv) === "undefined") {
        inputDiv = document.getElementsByTagName('body');   
    }

	inputDiv.appendChild(textField);

	return textField;
}



/* Function: addCanvas()
 * --------------------------
 * Creates and adds a new canvas to the center area of the webpage.
 *
 * Parameters: none
 */
GraphicsApp.prototype.addCanvas = function(width, height) {
    setBackground(width,height,0xFFFFFF);
}





/* Function: addTitle(title)
 * --------------------------------
 * Adds a title with the given text at the top of the page.
 *
 * Parameters:
 * -----------
 *	title: the text of the title to add.
 */
GraphicsApp.prototype.addTitle = function(title) {
	
	// Set the page title to be equal to the passed in text
 	var titleElem = document.createElement("TITLE");
 	titleElem.textContent = title;

 	var head = document.getElementsByTagName("HEAD")[0];
 	head.appendChild(titleElem);

 	// Also create and add an H1 element at the top displaying the passed in text
 	var h1 = document.createElement("H1");
 	h1.textContent = title;

 	var inputDiv = document.getElementById("inputDiv");
 	var body = document.getElementsByTagName("BODY")[0];
 	body.insertBefore(h1, inputDiv);
}





/* Function: displayErrorMessage(error)
 * --------------------------------
 * Displays an error message to the user in red below the text box.
 *
 * Parameters:
 * -----------
 *	error: the error message to display.
 */
GraphicsApp.prototype.displayErrorMessage = function(error) {
	var errorField = document.getElementById("errorField");
	errorField.innerHTML = error;
}




/* Function: getCurrentLocation()
 * ----------------------------
 * Calculates the user's current location, and calls callbackFn, passing
 * the user's current latitude and longitude.  The provided callbackFn should
 * therefore be something like 
 *
 * function callback(latitude, longitude) {
 *	...
 * }
 *
 *
 * Parameters:
 * -----------
 * callbackFn: the function that's called once the user's location has been calculated
 */
GraphicsApp.prototype.getCurrentLocation = function(callbackFn) {
	// Query the user's location
	navigator.geolocation.getCurrentPosition(function(position) {
		callbackFn(position.coords.latitude, position.coords.longitude);
	});
}



/* Function: fetchWeatherForQuery(query, numDays, successFn, errorFn)
 * -------------------------------------------------------------
 * Sends a request to the weather API, passing in the given query.
 *
 * Parameters:
 * -----------
 *	query: a string query of the place the weather should be fetched for.
 *
 *	numDays: the number of days for which you want to get the weather.
 *
 *	successFn: a function that takes a single parameter, the data returned from the API call.
 *	This function will be called upon success of the API call.
 *
 *	errorFn: a function that takes no parameters.  This function will be called upon failure of the API call.
 */
GraphicsApp.prototype.fetchWeatherForQuery = function(query, numDays, successFn, errorFn) {
	var url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=" + encodeURIComponent(query) + 
		"&mode=json&cnt=" + encodeURIComponent(numDays) + "&units=metric";
	this.sendWeatherRequestWithURL(url, successFn, errorFn);
}




/* Function: fetchWeatherForCoordinates(latitude, longitude, numDays, successFn, errorFn)
 * ----------------------------------------------------------------------------------
 * Sends a request to the weather API, passing in the given coordinates.
 *
 * Parameters:
 * -----------
 *	latitude: the latitude to fetch the weather for.
 *
 *	longitude: the longitude to fetch the weather for.
 *
 *	numDays: the number of days for which you want to get the weather.
 *
 *	successFn: a function that takes a single parameter, the data returned from the API call.
 *	This function will be called upon success of the API call.
 *
 *	errorFn: a function that takes no parameters.  This function will be called upon failure of the API call.
 */
GraphicsApp.prototype.fetchWeatherForCoordinates = function(latitude, longitude, numDays, successFn, errorFn) {
	var url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat=" + 
		encodeURIComponent(latitude) + "&lon=" + encodeURIComponent(longitude) + "&mode=json&cnt=" + encodeURIComponent(numDays) + "&units=metric";
	this.sendWeatherRequestWithURL(url, successFn, errorFn);
}

/*******************************************************/









/********* PRIVATE GraphicsApp METHODS ************/



/* Function: sendWeatherRequestWithURL(url, successFn, errorFn)
 * ---------------------------------------------------------
 * Makes an AJAX (Asynchronous Javascript and XML) GET request to the given URL.
 * If the request is unsuccessful, the errorFn callback is called.  If successful,
 * the weather server will return an array of objects, each representing the weather for
 * a day.  This function then adds the name of each day to each day object (eg. "Monday") and
 * passes the array to the successFn callback.
 *
 * Parameters:
 * -----------
 * 	url: the URL to send the request to.
 * 
 * 	successFn: the function to execute if a response is successfully returned.
 * 
 * 	errorFn: the function to execute if the request fails.
 */
GraphicsApp.prototype.sendWeatherRequestWithURL = function(url, successFn, errorFn) {
	
	// The handler for the AJAX requests that call the student's callbacks
	var obj = this;

	function xhrHandler() {
		if (this.readyState != 4) return;
		else if (this.status != 200 && errorFn) errorFn();
		else {
			var data = JSON.parse(this.responseText);

			var daysArray = data["list"];

			// If there is no data, call the error handler
			if (daysArray == null) {
				if (errorFn) errorFn();
				return;
			} else if (!successFn) return;

			var cleanedDaysArray = [];

			// Get the array of day names this weather data corresponds to
			var dayNames = obj.dayNamesStartingToday(daysArray.length);

			// Pull out only the relevant weather data and store an object for each
			// day inside of cleanedDaysArray
			for (var i = 0; i < daysArray.length; i++) {

				// Create a new day object with the relevant data inside
				var day = {};
				day["dayName"] = dayNames[i];
				day["tempHigh"] = daysArray[i]["temp"]["max"];
				day["tempLow"] = daysArray[i]["temp"]["min"];
				day["weatherDescription"] = daysArray[i]["weather"][0]["main"]; // Rain Clouds Clear Snow
				day["humidity"] = daysArray[i]["humidity"];
				day["windSpeed"] = daysArray[i]["speed"];

				// Add it to our days array
				cleanedDaysArray.push(day);
			}			

			successFn(cleanedDaysArray);
		}
	}

	// Create and send the request
	xhr = new XMLHttpRequest();
	xhr.onreadystatechange = xhrHandler;
	xhr.open("GET", url);
	xhr.send();	
}



/* Function: dayNamesStartingToday(numDays)
 * -------------------------------------
 * Returns an array of length "numDays" containing consecutive
 * weekday names starting with today.  For example, if today is
 * Tuesday, and numDays = 4, then dayNamesStartingToday would return
 * ["Tuesday", "Wednesday", "Thursday", "Friday"].
 *
 * Parameters:
 * -----------
 * 	numDays: the number day names to include in the array
 */
GraphicsApp.prototype.dayNamesStartingToday = function(numDays) {

	// Get the index of today
	var currDate = new Date();
	var todayIndex = currDate.getDay();

	var dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
	
	// Loop around the day names array starting today and add each day name
	var daysArray = [];
	for (var i = 0; i < numDays; i++) {

		// Loop around the day names array (if we get over 6, loop back around)
		var index = (todayIndex + i) % 7;
		daysArray.push(dayNames[index]);
	}

	return daysArray;
}

/****************************************/
