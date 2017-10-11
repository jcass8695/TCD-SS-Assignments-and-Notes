const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);

let username = '';

app.get('/', (req, res) => {
  res.sendFile(`${__dirname}/index.html`);
});

io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on('disconnect', () => {
    console.log('a user disconnected');
  });

  socket.on('chat message', (msg) => {
    if (msg.includes('username')) {
      username = msg.slice(msg.indexOf(' '), msg.length);
    } else {
      io.emit('chat message', username, msg);
    }
  });
});

http.listen(3000, () => {
  console.log('listening on *:3000');
});
