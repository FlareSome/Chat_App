import asyncio
from websockets import serve
import socketio
async def echo(websocket):
    # Iterate over incoming messages
    async for message in websocket:
        print(f"Received: {message}")
        # Send a message back
        await websocket.send(f"Echo: {message}")

async def main():
    # Start the server on localhost at port 8765
    async with serve(echo, "localhost", 8765) as server:
        print("Server running on ws://localhost:8765")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())