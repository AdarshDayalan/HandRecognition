# Wave
Computer Hand-Gesture Control 

## Purpose
Provide a more intuitive and intelligent method of computer navigation

## Description
Wave is a machine learning program that recognizes programmable hand poses and gestures and performs desired computer navigations.\
Basically you can control you computer with hand gestures.\
For example, a *wave* of your hand will switch tabs, a pointer finger controls the mouse, two fingers will scroll up or down, and much more.

## Demo

## How I made it

First I cleary wrote down what I wanted to make so I had a direct goal to work towards and then broke that goal down into manageble parts. 

### Goal
> Make a Computer Hand-Gesture Control system. Seemed very intimidating and overwhelming.

### Mental Breakdown
> I needed to classify hand poses and then I needed to make it navigate the computer. That's a little better.

> To classify hand poses, it first need to recognize a hand and then have a ML model output what pose the hand is in.

> To navigate the computer I can use make the program input keyboard shortcuts or move the mouse position to switch tabs, scroll, click, etc.

### Weekly Deadlines
| Week          | Objective                             | How I Acheived It                                                                    |
| ------------- |:-------------:                        | ---                                                                                  |
| Week 1        | Research                              | Researched Neural Networks, OpenCV, Tensorflow, and MediaPipe                        |
| Week 2        | Hand Recognition + Data Extraction    | Read documentation and implemented MediaPipe with python                             |
| Week 3        | ML model for pose classification      | Trained a ML model with Tensorflow with xyz coordinated of hand landmarks            |
| Week 4        | Test and train for more poses         | Added 14 poses with variation in the dataset and dropout layers to maximize accuracy |
| Week 5        | Add computer navigation functionality | Used windows libraries in python to control keyboard shortcuts and the mouse         |
| Week 6        | Test and fix bugs                     | Tested with various people, different lighting, and locations for generalization     |

## Problems

## Future

Right now to run this software you need python and all it's dependencies installed. This is very "bulky" and complicated for everyday users.

Moving forward, I want to integrate it on the .NET framewok and turn it into a computer application that runs in the background so it's more accessible and easier to use.

There can alse be options to program your own hand gestures and set it to do whatever mouse and keyboard inputs the user desires for more customization and personal experience.
