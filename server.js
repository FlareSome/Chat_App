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
usr_cnt=0
io.on('connection', (socket) => {
  usr_cnt++;
  console.log(`user${usr_cnt}: joined`)
  socket.on('chat_message', (msg) => {
    console.log(msg)
    io.emit('server_response', msg);
  });
});

server.listen(3000, () => {
  console.log('server running at http://localhost:3000');
});