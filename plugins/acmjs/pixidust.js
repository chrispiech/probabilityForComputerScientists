/*
* pixidust.js
* a collection of wrappers on pixi.js functionality for the sake 
* of making the interface more obvious for students who have
* been introduced to graphical programming by cs106A.
*
* Written by brycecr; github.com/brycecr
* except for the watch bit below
*/

/* HERE FOLLOWS A COOL WATCH HACK SO I CAN WATCH THINGS 
* It is included here for modularity. I don't want to 
* include another file in the html for the sake of keeping it 
* minimal and transparent for students. Pixidust is an all-or
* nothing package
*/
/*
* object.watch polyfill
*
* 2012-04-03
*
* By Eli Grey, http://eligrey.com
* Public Domain.
* NO WARRANTY EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.
*/
 
// object.watch
if (!Object.prototype.watch) {
Object.defineProperty(Object.prototype, "watch", {
enumerable: false
, configurable: true
, writable: false
, value: function (prop, handler) {
var
oldval = this[prop]
, newval = oldval
, getter = function () {
return newval;
}
, setter = function (val) {
oldval = newval;
return newval = handler.call(this, prop, oldval, val);
}
;
if (delete this[prop]) { // can't watch constants
Object.defineProperty(this, prop, {
get: getter
, set: setter
, enumerable: true
, configurable: true
});
}
}
});
}

 
// object.unwatch
if (!Object.prototype.unwatch) {
Object.defineProperty(Object.prototype, "unwatch", {
enumerable: false
, configurable: true
, writable: false
, value: function (prop) {
var val = this[prop];
delete this[prop]; // remove accessors
this[prop] = val;
}
});
}



/* HERE STARTS PIXIDUST
* LET THE GAMES BEGIN
*/ 



/* Init and Utility functions */

/* hack to let GObjects be treated like graphics elements
 * to the eyes of the stage */
PIXI.Stage.prototype.add = function(graphicsObject) {
    if (graphicsObject instanceof GObject) {
        this.addChild(graphicsObject.graphics);
        this.gobjects.push(graphicsObject);
    } else {
        this.addChild(graphicsObject);
    }
}

/* hack to let GObjects be treated like graphics elements
 * to the eyes of the stage */
PIXI.Stage.prototype.remove = function(graphicsObject) {
    if (typeof(graphicsObject) === 'undefined' 
        || graphicsObject === '')
        return;
    if (graphicsObject instanceof GObject) {
        this.removeChild(graphicsObject.graphics);
        var i = this.gobjects.indexOf(graphicsObject);
        if (i > -1) {
            this.gobjects.splice(i, 1);   
        }
    } else {
        try {
        this.removeChild(graphicsObject);
        } catch (err) {
            console.log("tried to remove something not on canvas "+err);
        }
    }
}

PIXI.Stage.prototype.getElementAt = function(x, y) {
    var children = stage.gobjects;
    for (var i=0; i<children.length; ++i) {
        var child = children[i];
        if (child.position.x < x && (child.position.x + child.width > x)
            && child.position.y < y && (child.position.y + child.height > y))
        {
            return children[i];
        }
    }
    return null;
}

function getElementAt(x,y) {
    if (typeof(stage) === 'undefined') {
        console.log('Tried to getElementAt without adding a stage first!');
        return;
    }
    stage.getElementAt(x,y);    
}

var stage;
var renderer;
function setBackground(width, height, color, canvas_id) {
        var checkLoad = function() {   
        document.readyState !== "complete" ? setTimeout(checkLoad,11) : function(){};   
    };  

    checkLoad();  
        
    /* SETUP */
    stage = new PIXI.Stage(0xFFFFFF); // make a white stage
    stage.gobjects = [];

    renderer = PIXI.autoDetectRenderer(width, height);

    document.getElementById(canvas_id).appendChild(renderer.view);

    renderer.view.onclick = function() {
        remove(clickToStartLabel);
        
        if (numlives < 3) {
            pause = false;
            pauseFunc();
        } else {
            requestAnimFrame(animate);
        }
    }

    //requestAnimFrame(animate);
        /* End Setup */
    return stage;
}

function animate() {
    requestAnimFrame(animate);
    if (typeof(drawFrame) === 'function') {
        drawFrame();
    }
    renderer.render(stage);
}

/* End init and utility funcitons */

/* GObject */
function GObject(startx,starty) {
    this.filled = true;
    this.graphics = new PIXI.Graphics();
    this.color = 0x000000;
    this.position = {x:startx, y:starty, gobject:this};
    this.position.watch('x', function(prop, oldval, newval) { 
        this.gobject.refresh(); 
        return newval;
    }); 
    this.position.watch('y', function(prop, oldval, newval) { 
        this.gobject.refresh(); 
        return newval;
    }); 
}

GObject.prototype = {
    setColor: function(color) { this.color = color; this.refresh(); },
    refresh: function() { 
        this.graphics.clear();
        if (this.filled) {
            this.graphics.beginFill(this.color);
        } else {
            this.graphics.lineStyle(1, this.color, 1.0);
        }
        this.draw();
        if (this.filled) {
            this.graphics.endFill(this.color);
        } 
    },
    draw: function() { /*ABSTRACT: override to draw something*/ },
    setPosition: function(x,y) { this.position.x = x; this.position.y; }
};
/* End GObject */

/* GRect */
function GRect(x, y, width, height) {
    GObject.call(this, x, y);
    this.width = width;
    this.height = height;
    this.refresh();
}

GRect.prototype = Object.create(GObject.prototype);
GRect.prototype.constructor = GRect;
GRect.prototype.getWidth = function() { return this.width; };
GRect.prototype.getHeight = function() { return this.height; };
GRect.prototype.setWidth = function(width) { this.width = width; this.refresh(); };
GRect.prototype.setHeight = function(height) { this.height = height; this.refresh(); };
GRect.prototype.draw = function() { this.graphics.drawRect(this.position.x, this.position.y, this.width, this.height); }
/* End GRect */

/* GOval */
function GOval(x, y, width, height) {
    GRect.call(this, x, y, width, height);
    this.refresh();
}

GOval.prototype = Object.create(GRect.prototype);
GOval.prototype.constructor = GOval;
GOval.prototype.draw = function() { this.graphics.drawEllipse(this.position.x, this.position.y, this.width/2, this.height/2); }
/* End GOval */

/* GCircle */
function GCircle(x, y, radius) {
    GOval.call(this, x, y, radius, radius);
    this.radius = radius;
    this.refresh();
}

GCircle.prototype = Object.create(GOval.prototype);
GCircle.prototype.constructor = GCircle;
GCircle.prototype.getRadius = function() { return this.radius; }
GCircle.prototype.setRadius = function(radius) { this.setRadiusX(radius); this.setRadiusY(radius); this.radius = radius; }
/* End GCircle */

/* Begin GImage */
function GImage(image_loc) {
    return PIXI.Sprite.fromImage('img/'+image_loc);           
}
/* End GImage. Wasn't that sweet? */

/* Begin GLabel */
function GLabel(str) {
   this.style = { font: "30px Verdana", fill: 0x000000, align: "left"};
    var text = new PIXI.Text(str, this.style);
    text.position.x = 0;
    text.position.y = 0;
    return text;
}

function GLabel(str, x, y) {
    this.style = { font: "30px Verdana", fill: 0x000000, align: "left"};
    var text = new PIXI.Text(str, this.style);
    text.position.x = x;
    text.position.y = y;
    return text;
}

PIXI.Text.prototype.setColor = function(color) {
    if (typeof(color) === "number" || typeof(color) === "Number") {
        color = '#' + ('00000' + (color | 0).toString(16)).substr(-6); 
    }
    this.style.fill = color;
    this.setStyle(this.style);   
}

PIXI.Text.prototype.setFont = function(font) {
    this.style.font = font;
    this.setStyle(this.style);
    this.updateText();
}

PIXI.Sprite.prototype.getWidth = function() {
    return this.width;
}

PIXI.Sprite.prototype.getHeight = function() {
    return this.height;
}

function add(obj) {
    if (typeof(stage) === 'undefined') {
        console.log("Tried to add an object without creating canvas first!");
        return;
    }
    stage.add(obj);
}

function remove(obj) {
    if (typeof(stage) === 'undefined') {
        console.log("Tried to add an object without creating canvas first!");
        return;
    }
    stage.remove(obj);
}

function removeAll() {
    for (var i = stage.children.length - 1; i >= 0; --i) {
        stage.removeChild(stage.children[i]);   
    }
}

PIXI.Sprite.prototype.setPosition = function(x,y) {
    this.position.x = x;
    this.position.y = y;
}

/* Cute solution from http://stackoverflow.com/questions/2532218/pick-random-property-from-a-javascript-object */
function pickRandomProperty(obj) {
    var result;
    var count = 0;
    for (var prop in obj)
        if (Math.random() < 1/++count)
           result = prop;
    return obj[result];
}

/* Colors! */
var Color = {'red': 0xFF0000, 'green': 0x00FF00, 'blue': 0x0000FF, 'cyan': 0x00FFFF, 'yellow': 0xFFFF00, 'white': 0xFFFFFF, 'black':0x000000, 'magenta':0xFF00FF,'orange':0xFFA500, 'pink':0xFFCBDB, 'gray':0x888888, 'light_gray':0xCCCCCC,'dark_gray':0x333333};
