import cv2
import mediapipe as mp
 
def main():
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(False, max_num_hands=4)
    mpDraw = mp.solutions.drawing_utils
 
    cap = cv2.VideoCapture(0)
    # print("starting cap")
    # wyze_url = "rtsp://wyze:adarsh123@192.168.86.21/live"
    # cap = cv2.VideoCapture(wyze_url)
    # print("Connected to cap")
 
    while (cap.isOpened()):
        _, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = cv2.resize(img, (960, 540))
        results = hands.process(imgRGB)
 
        if results.multi_hand_landmarks:
            for handLMS in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLMS, mpHands.HAND_CONNECTIONS)
 
        cv2.imshow("Image", img)
 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
if __name__ == '__main__':
    main()