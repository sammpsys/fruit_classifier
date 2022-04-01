'''

 Script to control the Jetank using multiple threads, based on input from UDP client

'''
from socket import *
import threading
import time
from time import sleep
from jetbot import Robot
from SCSCtrl import TTLServo

robot = Robot()
serverPort = 12000

# create UDP socket and bind to specified port
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print ("The UDP server is ready to recieve")


def move_forward():
    print("forward")
    robot.forward(0.2)
    time.sleep(1)
    robot.stop()

def stop():
    print("stop")
    robot.stop()


#     time.sleep(0.5)
#     robot.stop()

def move_backward():
    print("backwards")
    robot.backward(0.2)
    time.sleep(1)
    robot.stop()

#     time.sleep(0.5)
#     robot.stop()

def move_left():
    print("left")
    robot.left(0.3)
    time.sleep(0.5)
    robot.stop()


def move_right():
    print("right")
    robot.right(0.6)
    time.sleep(0.5)
    robot.stop()
    
def dance():
    robot.right(0.6)
    time.sleep(2)
    robot.forward(0.6)
    time.sleep(0.7)
    robot.backward(0.6)
    time.sleep(0.7)
    robot.left(0.6)
    time.sleep(2)
    robot.stop()

moveStartTor = 0.15    # The motor's initial rotation threshold. 
                       # The geared motor cannot rotate in the low PWM interval. 
                       # Long-term stall will reduce the motor's life.

fb_input = 0           # Store the speed parameter for the forward and backward direction.
lr_input = 0           # Store the parameters for steering.

servoCtrlTime = 0.001  # Delay after the TTL servo communication to avoid errors.
speedInput = 300       # Camera tilt and pan rotation speed.

armXStatus = 0         # The movement state of the X axis of the robotic arm (far and near direction).
armYStatus = 0         # The movement state of the Y axis of the robotic arm (vertical direction).
cameStatus = 0         # The movement state of the Camera.

goalX = 130            # Store the X-axis coordinate of the gripper of the robotic arm.
goalY = 50             # Store the Y-axis coordinate of the gripper of the robotic arm.
goalC = 0              # Store the position of camera.

xMax = 210             # Set the maximum X axis of the robotic arm.
xMin = 140             # Set the minimum X axis of the robotic arm.

yMax = 120             # Set the maximum Y axis of the robotic arm.
yMix = -120            # Set the minimum Y axis of the robotic arm.

cMax = 25              # Set the maximum position of the camera.
cMin = -45             # Set the minimum position of the camera.
cDan = 0               # Set the dangerous line of the camera.

movingTime = 0.005     # Set the running time between every two adjacent positions of the inverse kinematics function of the robotic arm.
movingSpeed = 10        # Set the movement speed of the robotic arm.

grabStatus = 0         # The movement state of the gripper.

cameraPosCheckMode = 1 # The switch of the camera position checking function, 1 - on, 0 - off.
                       # onec it is on, it can avoid the interference between the robotic arm and the camera.
cameraPosDanger = 0    # Whether the camera is in the danger zone.
cameraMoveSafe = 0     # Whether the camera has moved to the safe zone.    

def moveJetank(button_pressed):
    print("move Tank")
    if not moveTank.move_pressed:
        stop()
    else:
        if button_pressed == "w":
            move_forward()
        elif button_pressed == "s":
            move_backward()
        elif button_pressed == "a":
            move_left()
        elif button_pressed == "d":
            move_right()
        elif button_pressed == "q":
            stop()
        elif button_pressed == "dance":
            dance()
    moveTank.move_pressed = 0


# Control the gripping and loosening of the gripper.
def grabCtrlCommand(commandType):
    global grabStatus
    if not grabTank.grab_pressed:
        print("No new grab command")
    if commandType == 'g':
        commandLoose = 0
        commandGrab = 1
    elif commandType == 'l':
        commandGrab = 0
        commandLoose = 1

    if commandGrab and not grabStatus:
        TTLServo.servoAngleCtrl(4, -40, 1, 150)
        grabStatus = 1
        sleep(servoCtrlTime)
    elif commandLoose and grabStatus:
        TTLServo.servoAngleCtrl(4, 0, 1, 150)
        grabStatus = 0
        sleep(servoCtrlTime)
    grabTank.grab_pressed=0
    
# Robotic arm control function, for action execution (in another single thread).
def armCtrl(button_pressed):
    print("move Arm")
    global xMax, xMin, yMax, yMix, goalX, goalY, armXStatus, armYStatus
   # armCameraPosCheck()
    if not ctrlArm.arm_pressed:
        print("No new arm command")
    #    armStop()
    else:
        if button_pressed == "u":
            armXStatus = 1
            goalX += movingSpeed
            if goalX > xMax:
                goalX = xMax
            TTLServo.xyInputSmooth(goalX, goalY, movingTime)
            sleep(servoCtrlTime)
            ctrlArm.arm_pressed = 0
            return
        elif button_pressed == "j":
            armXStatus = 1
            goalX -= movingSpeed
            if goalX < xMin:
                goalX = xMin
            TTLServo.xyInputSmooth(goalX, goalY, movingTime)
            sleep(servoCtrlTime)
            ctrlArm.arm_pressed = 0
            return
        
        elif button_pressed == "h":
            armYStatus = 1
            goalY += movingSpeed
            if goalY > yMax:
                goalY = yMax
            if goalY > -50:
                cameraMoveSafe = 1
            TTLServo.xyInputSmooth(goalX, goalY, movingTime)
            sleep(servoCtrlTime)
            ctrlArm.arm_pressed = 0
            return
            
        elif button_pressed == "k":
            armYStatus = 1
            goalY -= movingSpeed
            if goalY < yMix:
                goalY = yMix
            if goalY > -50:
                cameraMoveSafe = 1
            TTLServo.xyInputSmooth(goalX, goalY, movingTime)
            sleep(servoCtrlTime)
            ctrlArm.arm_pressed = 0
            return


TTLServo.xyInputSmooth(goalX, goalY, 3)
TTLServo.servoAngleCtrl(1, 0, 1, 100)
TTLServo.servoAngleCtrl(4, 0, 1, 100)
TTLServo.servoAngleCtrl(5, 0, 1, 100)
sleep(3.5)
print('ready!')                

class ArmCtrlThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(ArmCtrlThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()
        self.button_pressed = ""
        self.arm_pressed = 0

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def run(self):
        while 1:
            self.__flag.wait()
            print("in arm while")
            #if self.arm_pressed:
            armCtrl(self.button_pressed)
            if not self.arm_pressed:
                self.pause()
            sleep(movingTime)


# Instantiate and start the multi-threaded servo control thread.
ctrlArm = ArmCtrlThread()
ctrlArm.start()

class moveThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(moveThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()
        self.button_pressed = ""
        self.move_pressed = 0

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def run(self):
        while 1:
            self.__flag.wait()
            print("in move while")
            moveJetank(self.button_pressed)
            if not self.move_pressed:
                self.pause()
            sleep(movingTime)


# Instantiate and start the multi-threaded servo control thread.
moveTank = moveThread()
moveTank.start()

class grabThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(grabThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()
        self.commandType = ""
        self.grab_pressed =0

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def run(self):
        while 1:
            self.__flag.wait()
            print("in grab while")
            grabCtrlCommand(self.commandType)
            if not self.grab_pressed:
                self.pause()
            sleep(movingTime)


# Instantiate and start the multi-threaded servo control thread.
grabTank = grabThread()
grabTank.start()

class inputThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(inputThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def run(self):
        while 1:
            self.__flag.wait()
            message, clientAddress = serverSocket.recvfrom(2048)
            mess = message.decode()
            print(mess)
            if mess == "w" or mess == "a" or mess == "s" or mess == "d" or mess == "q" or mess == "dance":
                print("Changing move variables")
                moveTank.button_pressed = mess
                moveTank.move_pressed = 1
                moveTank.resume()
            elif mess == "u" or mess == "j" or mess == "h" or mess == "k":
                print("Changing arm variables")
                ctrlArm.button_pressed = mess
                ctrlArm.arm_pressed = 1
                ctrlArm.resume()
            elif mess == "g" or mess == "l":
                print("Changing grab variables")
                grabTank.commandType=mess
                grabTank.grab_pressed=1
                grabTank.resume()
            


# Instantiate the gamepad input thread and start reading information
inputThreading = inputThread()
inputThreading.start()
inputThreading.resume()