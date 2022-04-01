# fruit_classifier

This project uses the Jetank (based on Nvidia Jetson Nano 4GB: https://jetbot.org/master/) to construct a device that can classify certain fruits in real time. The project also involves the use of remote control to move the fruit. 

## Table of Contents

- [Requirements](#requirements)
- [Description](#description)
- [Setup](#setup)
- [Maintainers](#maintainers)
- [Contributors](#contributors)

## Requirements

Requires Nvidia Jetson Nano 4GB as well as all the hardware components needed to construct the Jetank. For remote control, the project also requires `Python3` and   an Python IDE, prefereably `PyCharm`. 

## Description
There are three main elements to this project: machine learning, fruit classification and remote control.

### Machine learning
The VGG-16 network was trained in an Anaconda environment. Only the last layer was trained. The dataset used was the following:           https://www.kaggle.com/datasets/balraj98/apple2orange-dataset. Only two classes were trained; apples and oranges. It would have been ideal to train more classes, but this was not possible due to time constraints. The training code is based on a similar implementation that I made during a machine learning course at Chalmers University of Technology. The training is presented in a notebook called training.ipynb.

### Fruit classification
The fruit_classification notebook contains the real-time fruit classifer. It uses the previously trained VGG-16. Much of the code in the notebook is based on a tutorial provided by Nvidia called motion_Detect_en.ipynb. It is found in jetbot/notebooks/JETANK_3_motionDetect/motionDetect_en.ipynb on the Jetank. It should be noted that the camera in the fruit classification notebook is prone to lag. Additionally, the camera works best when the fruit is close to the camera, between 10-20 cm distance from the camera. It is presented in a notebook called fruit_classifier.ipynb.

### Remote Control
This portion consists of two Python files - socket_connect.py and remote_control.py. The code is based on a previous assignment that was done in the assignment in conjunction with another student, Hannes Ringblom. The code is based on Nvidia's gamepadCtrl notebook found in jetbot/notebooks/JETANK_6_gamepadCtrl/gamepadCtrl_en.ipynb. 

A UDP connection is used to send messages between a client (user's computer) and the server (Jetank). Thus, the Jetank can be controlled using the computer.

## Setup

### Hardware
The hardware required for this project is the following: Nvidia Jetson Nano 4GB, Jetson Developer Kit, 3 18650 batteries and a Micro-USB to USB-A cable. 

### Jetank
To setup the Jetank follow the steps in this guide: https://www.youtube.com/watch?v=qNy1hulFk6I. This guide includes instructions for downloading and flashing the Jetbot SD card images. The version of Jetpack used in this project is 4.5. 

### Fruit classification
The neural network that is used on the Jetank in classifying fruits in real time uses Pytorch v1.8, Torchvision v0.9.0 and Python 3.6. The necessary packages can be installed using https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-10-now-available/72048. The pre-trained model can be downloaded from (Github doesn't allow files larger than 50 MB): https://drive.google.com/file/d/1FZnoECT0d64aDwrZF2BZ0AHCo4NZ0yJg/view?usp=sharing. Press download in the top right right corner.

### Remote Control
Upload remote_control.py to your Jetank. Save socket_connect somewhere on your local machine. It is recommended that you run remote_control.py first in the JupyterLab terminal of the Jetank first and then run socket_connect.py in Pycharm on your machine. Remember that you need to change the IP-address in socket_connect.py to the one matching your Jetank. This can be run in tandem with the fruit_classifier notebook.

### Training/Retraining
The VGG-16 network was trained in an Anaconda environment. It is not necessary to perform your own training to run the fruit_classifer.ipynb in real time. However, if one wishes to conduct one's own training, it is recommeded that one uses Anaconda 2021.11 with Pytorch 1.11.0 and Torchvision 0.12.0. It is recommended that you reorganize the folder into the following structure: /images/train/apples/, /images/train/oranges/, /images/val/apples/, images/val/oranges/. 

## Maintainers
[Sam @sammpsys](https://gitlab.com/sammpsys)

## Contributors
[Sam @sammpsys](https://gitlab.com/sammpsys)
