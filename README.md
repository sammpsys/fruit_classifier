# fruit_classifier

This project uses the Jetank (based on Nvidia Jetson Nano 4GB: https://jetbot.org/master/) to construct a device that can classify certain fruits in real time. The project also involves the use of remote control to move the fruit. 

## Table of Contents

- [Requirements](#requirements)
- [Description](#description)
- [Setup](#setup)
- [Reflections](#reflections)
- [Maintainers](#maintainers)
- [Contributors](#contributors)

## Requirements

Requires Nvidia Jetson Nano 4GB as well as all the hardware components needed to construct the Jetank. For remote control, the project also requires `Python3` and   an Python IDE, prefereably `PyCharm`. 

## Description
There are three main elements to this project: machine learning, fruit classification and remote control.

### Machine learning
The VGG-16 network was trained in an Anaconda environment. Only the last layer was trained. The dataset used was the following:           https://www.kaggle.com/datasets/balraj98/apple2orange-dataset. Only two classes were trained; apples and oranges. It would have been ideal to train more classes, but this was not possible due to time constraints. The training code is based on a similar implementation that I made during a machine learning course at Chalmers University of Technology. The training is presented in a notebook called training.

### Fruit classification
The fruit_classification notebook contains the real-time fruit classifer. It uses the previously trained VGG-16. Much of the code in the notebook is based on a tutorial provided by Nvidia called motion detection. It should be noted that the camera in the fruit classification notebook is prone to lag. Additionally, the camera works best when the fruit is close to the camera, between 10-20 cm distance from the camera. 

### Remote Control
This portion consists of two Python files - socket_connect.py and remote_control.py. The code is based on a previous assignment that was done in the assignment in conjunction with another student, Hannes Ringblom. The code is based on Nvidia's Gamepad tutorial. 

A UDP connection is used to send messages between a client (user's computer) and the server (Jetank). Thus, the Jetank can be controlled using the computer. It is recommended that you run remote_control.py first in the JupyterLab terminal of the Jettank first and then run socket_connect.py on your machine. Remember that you need to change the IP-address in the script to the one matching your Jettank. 

## Setup

### Hardware
The hardware required for this project is the following: Nvidia Jetson Nano 4GB, Jetson Developer Kit, 3 18650 batteries and a Micro-USB to USB-A cable. 

### Jetbot
To setup the Jetank follow the steps in this guide: https://www.youtube.com/watch?v=qNy1hulFk6I. This guide includes instructions for downloading and flashing the Jetbot SD card images. The version of Jetpack used in this project is 4.5. 

### Machine learning
The neural network that is used on the Jetbot in classifying images in real time uses Pytorch v1.8, Torchvision v0.9.0 and Python 3.6. The necessary packages can be installed using https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-10-now-available/72048. 

### Training/Retraining
The VGG-16 network was trained in an Anaconda environment. It is not necessary to perform your own training to run the classifier in real time. However, if one wishes to conduct one's own training, it is recommeded that one uses Anaconda 2021.11 with Pytorch 1.11.0 and Torchvision 0.12.0. It is recommended that you reorganize the folder into the following structure: /images/train/apples/, /images/train/oranges/, /images/val/apples/, images/val/oranges/.

## Reflections
This project is not as advanced as it could be. There are several reasons for this:

1. Many different machine learning models were tested until a good one was found. This process took a lot of time which led to further complications down the line.
2. There were issues with the camera on several instances. This necessitated a reflashing of the image which delayed the work.
3. Initially, an object detection model (such as YoloV3 and SSD-mobilenet) was pursued. However, these models were not compatiable with the version of the image on the SD card.
4. I had issues with using the office network. I was able eventually to solve this issue using an alternative method but it took several days to solve.
5. When I eventually deployed my model on the Jetank, I had compatibility issues with Pytorch. I eventually found out which versions of Pytorch and Torchvision are compatible with Jetpack 4.5. 

## Maintainers
[Sam @sammpsys](https://gitlab.com/sammpsys)

## Contributors
[Sam @sammpsys](https://gitlab.com/sammpsys)
