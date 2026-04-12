const express = require('express');
const { createServer } = require('node:http');
const { join } = require('node:path');
const { Server } = require('socket.io');

const app = express();
const server = createServer(app);
const io = new Server(server);

app.get('/', (req, res) => {
  res.json({'username': 'username101',
            'message': 'hello world'
  });
});

io.on('connection', (socket) => {
  socket.on('chat message', (msg) => {
    // Broadcast the message to all other connected clients
    socket.broadcast.emit('chat message', msg);
  });
});

server.listen(3000, () => {
  console.log('server running at http://localhost:3000');
});