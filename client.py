# client.py
import socketio

# Create a Socket.io client instance
sio = socketio.Client()

@sio.event
def connect():
    print("Successfully connected to the server!")

@sio.event
def disconnect():
    print("Disconnected from server")

# Listen for the 'server_response' event
@sio.on("server_response")
def on_message(data):
    print("Server says:", data)

# Connect to the Node.js server
sio.connect("http://localhost:3000")

# Emit a message to the 'chat_message' event
sio.emit("chat_message", {"user": "Python", "text": "Hello from the other side!"})

    print(data["user"],": ",data["text"])

# Connect to the Node.js server


# Emit a message to the 'chat_message' event
username=input("Enter Username: ")
sio.connect("http://localhost:3000")
while(True):
    message = input()
    print("\033[A\033[K", end="")     
    sio.emit("chat_message", {"user": username, "text": message})





# Keep the connection alive
sio.wait()
