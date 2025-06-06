import asyncio
import websockets
import serial

# Constants
PORT = 8765

# Serial connection to the Arduino Nano
serial = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

async def connect(websocket):
    print("[*] Connection Established!")
    
    # Listen for commands
    while True:
        try:
            # Wait for a command
            command = await websocket.recv(4)
            print(f"[*] Recieved: {command}")

            # Do something about the recieved command her
            
            if command[1] == "1":
                serial.write(b'\xff\xff\xff\xff\xff\xff')
            elif command[2] == "1":
                serial.write(b'\x00\x00\x00\x00\x00\x00')
            else:
                serial.write(b"\x7f\x7f\x7f\x7f\x7f\x7f")

        except websockets.exceptions.ConnectionClosed as e:
            print(f"[*] Connection Closed: {e}")
            break


async def main():
    async with websockets.serve(connect, "0.0.0.0", PORT):
        print(f"[*] Server Started on Port {PORT}")
        await asyncio.Future() # run forever


# Start the Server
if __name__ == "__main__":
    asyncio.run(main())

