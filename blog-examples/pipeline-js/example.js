// For this example use the very handy pipeline-js
var Pipeline = require('pipeline-js');

// Our functions
function add5(x)   { return x + 5; }
function square(x) { return x * x; }
function div4(x)   { return x/4; }

console.log("Make pipeline...")
var pipeline = new Pipeline([add5, square, div4]);

console.log("Push 5 through pipeline: " + pipeline.process(5));
