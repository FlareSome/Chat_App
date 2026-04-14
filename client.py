import socketio

# Create a Socket.IO client
sio = socketio.Client()

# When connected
@sio.event
def connect():
    print("Connected to server!")

# When disconnected
@sio.event
def disconnect():
    print("❌ Disconnected from server")

# Listen for messages from server
@sio.on("server_response")
def on_message(data):
    print(f"{data['user']}: {data['text']}")

def main():
    username = input("Enter Username: ")

    # Connect to server
    sio.connect("http://localhost:3000")

    print("Start chatting (Ctrl+C to exit)\n")

    try:
        while True:
            message = input()
            sio.emit("chat_message", {
                "user": username,
                "text": message
            })
    except KeyboardInterrupt:
        print("\nExiting chat...")
        sio.disconnect()

# Run program
if __name__ == "__main__":
    main()
    sio.wait()