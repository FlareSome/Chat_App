const express = require('express');
const { createServer } = require('node:http');
const { Server } = require('socket.io');

const app = express();
const server = createServer(app);
const io = new Server(server);

// Health check endpoint
app.get('/', (req, res) => {
  res.json({'status': 'online', 'server': 'ChatApp_v2'});
});

io.on('connection', (socket) => {
  // Silent connection for TUI stability
  socket.on('chat_message', (msg) => {
    // Broadcast to all connected clients
    io.emit('server_response', msg);
  });
});

server.listen(3000, '0.0.0.0', () => {
  console.log('Chat Server running on http://localhost:3000');
});