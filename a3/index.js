var express = require('express');
var path = require('path');
var app = express();

app.use(express.static(__dirname))
app.get('/', (req, res) => {
    res.sendFile('index.html');
});

app.listen(5050);
