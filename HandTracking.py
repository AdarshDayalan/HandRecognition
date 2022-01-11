import cv2
import csv
import mediapipe as mp
import numpy as np
import copy
import itertools
import math
import time

import HandModel
from threading import Thread

import constants
from constants import label_names

from key_press import swipe, scroll, mouse, press

motion_data = []
motion_data_0 = []

def calculateDistance(p1, p2):
    dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p2[1])**2)
    return dist
 
def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
 
    landmark_array = np.empty((0, 2), int)
 
    for _, landmark in enumerate(landmarks.landmark):
        # print(landmark)
 
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point = [np.array((landmark_x, landmark_y))]
        landmark_array = np.append(landmark_array, landmark_point, axis=0)
 
    # print("\n")
    x, y, w, h = cv2.boundingRect(landmark_array)
 
    return [x, y, x + w, y + h]
 
def draw_bounding_rect(use_brect, image, brect, text):
    if use_brect:
        # Outer rectangle
        cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                     (0, 0, 0), 1)
        cv2.putText(image, text, (brect[0], brect[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
 
    return image

def draw_running(image, run):
    running = "Off"
    color = (0,0,255)
    if(run):
        running = "On"
        color = (0,255,0)
    cv2.putText(image, "Running: " + running, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
 
def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
 
    landmark_point = []
 
    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z
 
        landmark_point.append([landmark_x, landmark_y])
 
    return landmark_point
 
def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)
 
    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]
 
        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
 
    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))
 
    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))
 
    def normalize_(n):
        return n / max_value
 
    temp_landmark_list = list(map(normalize_, temp_landmark_list))
 
    return temp_landmark_list

def process_hand(img, handLMS):
    # mpDraw.draw_landmarks(img, handLMS, mpHands.HAND_CONNECTIONS)
    text = "None"
    # #Normalizes Data
    lml = calc_landmark_list(img, handLMS)
    pre_lml = pre_process_landmark(lml)
    pre_lml = (np.expand_dims(pre_lml,0))
    probability_values = HandModel.probability_model.predict(pre_lml)[0]
    # logging_csv('Data/probability.csv', probability_values)
    #Adarsh
    if(np.max(probability_values) > 0.9):
        constants.current_state = np.argmax(probability_values)
        if(constants.change_state):
            if(label_names[constants.current_state] == "one"):
                if(len(motion_data) < 10):
                    motion_data.append([lml[8][0], lml[8][1]])
                    motion_data_0.append([lml[0][0], lml[0][1]])
                else:
                    motion_data.pop(0)
                    motion_data_0.pop(0)
                    motion_data.append([lml[8][0], lml[8][1]])
                    motion_data_0.append([lml[0][0], lml[0][1]])
                if(len(motion_data) == 10):
                    upper = len(motion_data)-1
                    lower = len(motion_data)-4
                    x = motion_data[upper][0] - motion_data[lower][0]
                    y = motion_data[lower][1] - motion_data[upper][1]

                    # x_in_range = True
                    # for i in range(len(motion_data)):
                    #     if abs(motion_data[0][0] - motion_data[i][0]) > 20 or abs(motion_data_0[0][0] - motion_data_0[i][0]) > 10 or abs(motion_data_0[0][1] - motion_data_0[i][1]) > 10:
                    #         x_in_range = not x_in_range
                    #         break
                    
                    # if(x_in_range):
                    #     y_change_up = abs(motion_data[int(len(motion_data)/2)][1] - motion_data[len(motion_data)-1][1])
                    #     y_change_down = motion_data[0][1] - motion_data[int(len(motion_data)/2)][1]
                    #     if y_change_down < -20 and y_change_up > 20:
                    #         press("Left Click")
                    #         print("Click")
                    # else:
                    #     mouse(int(x), int(y))
                        # if(start_change < 5 and y_change > 20):
                        #     press("Left Click")
                        #     print("Click")

                    # if(abs(x) < 1 and abs(y) < 1):
                    #     if(constants.click_ready):
                    #         constants.click_time = time.time()
                    #         constants.click_ready = False
                    #     if(time.time() - constants.click_time >= 2):
                    #         press("Left Click")
                    #         constants.click_ready = True
                    
                    # x,y = motion_data[4][0], motion_data[4][1]
                    # width, height = img.shape[1], img.shape[0]
                    # x = (x/(2*width)) * constants.screen_width
                    # y = (y/(2*height)) * constants.screen_height
                    mouse(int(x), int(y))

                for i in range(len(motion_data)):
                    multiplier = i/len(motion_data)
                    cv2.circle(img, (motion_data[i][0], motion_data[i][1]), 10,
                    (multiplier * 152, multiplier* 251, multiplier * 152), 2)
            else:
                if(len(motion_data) != 0):
                    motion_data.clear()
            if label_names[constants.current_state] == "brightness":
                dist = calculateDistance(lml[8], lml[4])
                total = calculateDistance(lml[8], lml[5])
                multiplier = 1
                if(total != 0):
                    multiplier = dist/total
                    # print(round(multiplier/2, 1))
                cv2.line(img, lml[8], lml[4], (multiplier * 152, multiplier* 251, multiplier * 152), 2)
            
            elif label_names[constants.current_state] == "two":
                dist_y = lml[8][1] - lml[5][1]
                total = calc_bounding_rect(img, handLMS)
                total = total[0] - total[2]
                multiplier = 1
                if(total != 0):
                    multiplier = dist_y/total
                    scroll(multiplier)
                cv2.line(img, lml[8], lml[5], (multiplier * 152, multiplier* 251, multiplier * 152), 2)
            
            elif label_names[constants.current_state] == "L":
                if(label_names[constants.previous_state] == "one"):
                    press("Left Click")
            elif label_names[constants.current_state] == "front swipe":
                if(label_names[constants.previous_state] == "back swipe"):
                    constants.swipe_time = time.time()
                    swipe("Swipe Right")
                    constants.release = True

            elif label_names[constants.current_state] == "open down":
                if(label_names[constants.previous_state] == "open up"):
                    press("Close Tab")
            # elif label_names[constants.current_state] == "back swipe":
            #     # print("See back")
            #     if(label_names[constants.previous_state] == "front swipe"):
            #         constants.swipe_time = time.time()
            #         swipe("Swipe Left")
            #         constants.release = True
            elif label_names[constants.current_state] == "two front swipe":
                if(label_names[constants.previous_state] == "two back swipe"):
                    constants.swipe_time = time.time()
                if(time.time() - constants.swipe_time > 0.5):
                    constants.swipe_time = time.time()
                    swipe("Tab Right")
            elif label_names[constants.current_state] == "two back swipe":
                if(label_names[constants.previous_state] == "two front swipe"):
                    constants.swipe_time = time.time()
                if(time.time() - constants.swipe_time > 0.5):
                    constants.swipe_time = time.time()
                    swipe("Tab Left")
            
        if(constants.current_state != constants.previous_state):
            if(constants.previous_state == 11 and constants.current_state == 1):
                constants.change_state = True
            elif(constants.current_state == 11):
                print(label_names[constants.current_state])
                constants.previous_state = 1
                constants.change_state = False
            if(constants.change_state):
                print(label_names[constants.current_state])
            constants.previous_state = constants.current_state
        if(constants.change_state):
            text = label_names[constants.current_state] + " " + str(np.max(probability_values))


    return text

def logging_csv(csv_path, data):
    with open(csv_path, "w") as f:
        w = csv.writer(f)
        w.writerow(data)

 
def main():

    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,max_num_hands=1,min_detection_confidence=0.5)
    
    cap = cv2.VideoCapture(0)

    constants.change_state = False

    constants.swipe_time = time.time()
    
    while (cap.isOpened()):
        success, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        # img = cv2.resize(img, (960, 540))
        draw_running(img, constants.change_state)
        if results.multi_hand_landmarks:
            for handLMS in results.multi_hand_landmarks:
                text = process_hand(img, handLMS)
                b_rect = calc_bounding_rect(img, handLMS)
                img = draw_bounding_rect(True, img, b_rect, text)

        if(time.time() - constants.swipe_time) > 1 and constants.release:
            print("RElease alt")
            swipe("Done Swipe")
            constants.release = False

        cv2.imshow("Image", img)
 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
if __name__ == '__main__':
    main_thread = Thread(target = main)
    main_thread.start()
    main_thread.join()
