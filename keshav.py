import asyncio
import websockets
import serial
import time
from adafruit_servokit import ServoKit


"""This is a template code to be completed when we set up the servos completely"""

import numpy as np
def_angle = 90
turn_angle = 3

LENGTH = 400
WIDTH = 300

def get_radius(angle):
    return LENGTH / np.tan(np.deg2rad(angle))


"""
The way this will work is by assigning a wanted angle to the side it is turning to:
So if based on the angle, we are turning left, we will assign the left side to turn that much
Similarly for turning right

And then we will calculate the radiuses necessary for the inner and outer wheels.
Based on this we will calculate and assign the angles to the servos
"""

# Example of how the servos would be controlled
kit = ServoKit(channels=16)

wheels = [
    kit.servo[0],  # front-left
    kit.servo[1],  # mid-left   (unused by Rover.turn())
    kit.servo[2],  # rear-left
    kit.servo[3],  # front-right
    kit.servo[4],  # mid-right  (unused by Rover.turn())
    kit.servo[5],  # rear-right
]

class Rover():
    def __init__(self, wheels, max_turn_angle):
        '''
        Initialize the rover's parameters
        wheels => list of wheels (1st 3 on the left, the other 3 on the right side of the rover)
        '''
        self.r1 = 1
        self.r2 = 1
        self.wheels = wheels

        self.max_turn_angle = max_turn_angle
        self.angle = 0

    
    def turn(self, a):
        '''
        turn the rover by `a` degrees counter clockwise
        '''

        self.angle += a
        if abs(self.angle) > self.max_turn_angle:
            self.angle = (self.angle / abs(self.angle)) * self.max_turn_angle
        if abs(self.angle) < 0:
            self.angle = (self.angle / abs(self.angle)) * 0

        # check which way the rover is turning
        if  self.angle > 0:# and self.angle < self.max_turn_angle:
            # if turning to the left
            try:
                  self.wheels[0].angle = self.angle + def_angle
            except Exception:
                  print("Yippee")
            self.r1 = get_radius(self.angle)  # Inner radius
    
            # Calculate the outer radius (for outer front wheel)
            self.r2 = get_radius(self.angle) + WIDTH / 2  # Outer radius
            
            # Calculate the outer wheel angle (for outer front wheel)
			
            try:
                self.wheels[3].angle = np.rad2deg(np.arctan(LENGTH / self.r2)) + def_angle  # Outer right wheel angle
            except Exception:
                print("Max Angle Reached")

            # Rear wheels (steering in opposite direction for sharper turn)
            self.wheels[2].angle = 180 - self.wheels[0].angle  # Rear left wheel
            
            
            self.wheels[5].angle = 180 - self.wheels[3].angle  # Rear right wheel
			
        elif self.angle < 0:# and self.angle > -self.max_turn_angle:
            # if turning to the right
            try:  
                self.wheels[3].angle = self.angle + def_angle
            except Exception:
                  print("Yippee")
            self.r1 = get_radius(self.angle)  # Inner radius
    
            # Calculate the outer radius (for outer front wheel)
            self.r2 = get_radius(self.angle) - WIDTH / 2  # Outer radius
            
            # Calculate the outer wheel angle (for outer front wheel)
            self.wheels[0].angle = np.rad2deg(np.arctan(LENGTH / self.r2)) + def_angle # Outer right wheel angle
            
            # Rear wheels (steering in opposite direction for sharper turn)
            self.wheels[2].angle = 180 - self.wheels[0].angle  # Rear left wheel
            
            try:
                self.wheels[5].angle = 180 - self.wheels[3].angle  # Rear right wheel
            except Exception:
                print("Max Angle Reached")


# Constants
PORT = 8765

# Serial connection to the Arduino Nano
serial = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

async def connect(websocket):
	rover = Rover(wheels=wheels, max_turn_angle=90)
	print("[*] Connection Established!")
	# Listen for commands
	while True:
		try:
			outer_speed = 255
			inner_speed = int(outer_speed/rover.r2*rover.r1)
			# Wait for a command
			command = await websocket.recv(4)
			print(f"[*] Received: {command}")

			# Rover.turn(1)

			# Do something about the received command her

			if command[1] == "1":       # w
				pass
				#serial.write(b'\xff\xff\xff\xff\xff\xff')
			elif command[2] == "1":     # s
				pass
				#serial.write(b'\x00\x00\x00\x00\x00\x00')
			else:
				pass
				#serial.write(b"\x7f\x7f\x7f\x7f\x7f\x7f")
			if command[3] == "1":       # d
				# right = bytearray([outer_speed, outer_speed, outer_speed, inner_speed, inner_speed, inner_speed])
				rover.turn(-turn_angle)
				#serial.write(right)
			if command[0] == "1":       # a
				# left = bytearray([inner_speed, inner_speed, inner_speed, outer_speed, outer_speed, outer_speed])
				rover.turn(turn_angle)
				#serial.write(left)

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
