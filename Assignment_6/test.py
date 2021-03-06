import threading

import numpy as np
import cv2 as cv
import time


class FaceDetection:
    image_width = 0
    image_height = 0
    time_since_talk = 16.0
    time_start = False
    horizontal = 1500
    vertical = 1500
    head_increment_horizontal = 1497
    search_for_face_inc = 1510
    search_for_face_up = True
    wheels_value = 6000
    wheels_inc = 50
    turn_inc = 50
    turn_value = 6000
    face_cascade = cv.CascadeClassifier(
        'haarcascade_frontalface_default.xml')

    def __init__(self):
        # Sourced from https://ecat.montana.edu/d2l/le/content/524639/viewContent/3826523/View
        cap = cv.VideoCapture(0)
        # cv.namedWindow("Video")
        while True:
            status, image = cap.read()
            self.image_height, self.image_width, _ = image.shape

            self.detect_face(image)
            # cv.imshow("Video", img)
            cv.imshow('Face Detection', image)
            k = cv.waitKey(1)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        cv.destroyAllWindows()

    #     eye_cascade = cv.CascadeClassifier('/usr/local/lib/python3.6/dist-packages/cv2/data/haarcascade_eye.xml')
    # ascade = cv.CascadeClassifier('/usr/local/lib/python3.6/dist-packages/cv2/data/haarcascade_smile.xml')
    #

    #
    # def talk(self):
    #     print("robot speak")
    #     IP = '10.200.48.77'
    #     PORT = 5010
    #     speak = client.ClientSocket(IP, PORT)
    #     # speak.start()
    #     time.sleep(1)
    #     speak.sendData("Hello Human")

    def detect_face(self, img):
        # Sourced from https://ecat.montana.edu/d2l/le/content/524639/viewContent/3947225/View
        # faces = self.face_vars(img.copy())
        time_for_human = 5.0  # Variable setting the time between detecting a new human
        gray = cv.cvtColor(img.copy(), cv.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.09, 10)
        # faces = []
        # faces = face_cascade.detectMultiScale(gray, 1.9, 5)
        # print(faces)
        if len(faces) > 0:

                # self.time_since_talk = time.time()

            #                    self.talk()
            for (x, y, w, h) in faces:
                cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                self.time_since_talk = time.time()
                self.center(x, y, w, h)
                if self.horizontal < 5800:
                    self.increment_Movement("left", 2110, 7400, self.turn_inc, 0)
                elif self.horizontal > 6200:
                    self.increment_Movement("right", 2110, 7400, self.turn_inc, 0)
                elif self.turn_value != 6000:
                    print("Stop wheels")
                if (time.time() - self.time_since_talk) > time_for_human or not self.time_start:
                    self.time_start = True
                    print("Hello Human")

        else:  # Enters to search for human face
            # self.search_for_face()
            self.increment_Movement("head", 1510, 7500, 599, 1198)

    def center(self, x, y, face_w, face_y):
        left = self.image_width * .55
        right = self.image_width * .45
        up = self.image_height * .45
        down = self.image_height * .55

        x_center = x + (face_w / 2)
        y_center = y + (face_y / 2)
        head_inc = 300
        move_needed = False

        if x_center > left:
            move_needed = True
            self.horizontal -= head_inc
            # print("move left")
        elif x_center < right:
            move_needed = True
            # print("move right")

            self.horizontal += head_inc
        if y_center < up:
            move_needed = True
            # print("move up")

            self.vertical += head_inc
        elif y_center > down:
            move_needed = True
            # print("move down")

            self.vertical -= head_inc
        if move_needed:
            min = 1510
            max = 7500
            # Verifies values are within bounds.
            if self.vertical < min:
                self.vertical = min
            elif self.vertical > max:
                self.vertical = max
            if self.horizontal < min:
                self.horizontal = min
            elif self.horizontal > max:
                self.horizontal = max
            threading.Thread(target=self.move_head).start()
        else:
            pass
            #print("centered")
        if face_w < 150:
            # self.robot.move_wheels("move", 7000)
            # threading.Thread(target=self.move_forward).start()
            self.increment_Movement("forward", 1510, 7500,self.wheels_inc, 0)
        elif face_w > 250:
            self.increment_Movement("backward", 1510, 500, self.wheels_inc, 0)
        elif self.wheels_value != 6000:
            self.wheels_value = 6000
            print("stop wheels ", self.wheels_value)

    def move_head(self):
        #        self.robot.move_head(self.horizontal, self.vertical)
        print("horizontal: ", self.horizontal, "vertical: ", self.vertical)
        pass

    # time.sleep(.5)
    # moves = {"right": self.headRight, "left": self.headLeft, "up": self.headUp,
    #          "down": self.headDown}  # ["right", "left", "up", "down"]
    # moves[movement].__call__()

    # def face_vars(self, img):
    #     face_cascade = cv.CascadeClassifier(
    #         '/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
    #     faces = face_cascade.detectMultiScale(img, 1.09, 9)
    #     # if len(faces) < 1:
    #     #     faces = self.search_for_face(face_cascade, gray)

    #     return faces
    def move_forward(self):
        print("Move robot forward. ", self.wheels_value)

    def move_backward(self):
        print("Move robot forward. ", self.wheels_value)
    def turn_wheels(self):
        print("turn wheels")

    # def search_for_face(self):
    #     head_inc_value = 599
    #     head_increment_vert = 1198
    #     head_max = 7500
    #     head_min = 1510
    #     self.horizontal = self.search_for_face_inc
    #     if self.horizontal > head_max:  # Checks if head has reached farthest right value
    #         self.search_for_face_inc = head_max
    #         self.search_for_face_up = False  # Sets to false to head the other direction
    #         self.horizontal = self.search_for_face_inc  # Sets the face value iin case it is greater than 7500
    #         self.vertical += head_increment_vert  # Increments the vertical position
    #     elif self.horizontal < head_min:  # Checks if head is in the farthest left postion
    #         self.search_for_face_inc = head_min
    #         self.search_for_face_up = True  # Sets true to start heading the other way.
    #         self.horizontal = self.search_for_face_inc  # Sets incase head is less than 1519
    #         self.vertical += head_increment_vert  # Increments the vertical postition
    #
    #     if self.vertical > head_max:  # Resets to bottom vertical position
    #         self.vertical = head_min
    #     if self.search_for_face_up:
    #         self.search_for_face_inc += head_inc_value
    #     else:
    #         self.search_for_face_inc -= head_inc_value
    #     self.move_head()

    def increment_Movement(self, move, min, max, inc1, inc2): # iteratively moves robot.
        moves = {"head": self.move_head, "forward": self.move_forward, "backward": self.move_backward, "left": self.turn_wheels, "right": self.turn_wheels}

        if move == "head":
            self.horizontal = self.search_for_face_inc
            if self.horizontal > max:  # Checks if head has reached farthest right value
                self.search_for_face_inc = max
                self.search_for_face_up = False  # Sets to false to head the other direction
                self.horizontal = self.search_for_face_inc  # Sets the face value iin case it is greater than 7500
                self.vertical += inc2  # Increments the vertical position
            elif self.horizontal < min:  # Checks if head is in the farthest left postion
                self.search_for_face_inc = min
                self.search_for_face_up = True  # Sets true to start heading the other way.
                self.horizontal = self.search_for_face_inc  # Sets incase head is less than 1519
                self.vertical += inc2  # Increments the vertical postition

            if self.vertical > max:  # Resets to bottom vertical position
                self.vertical = min
            if self.search_for_face_up:
                self.search_for_face_inc += inc1
            else:
                self.search_for_face_inc -= inc1
        elif move == "forward":
            self.wheels_value -= inc1
            if self.wheels_value > max:
                self.wheels_value = max
            elif self.wheels_value < min:
                self.wheels_value = min
        elif move == "backward":
            self.wheels_value += inc1
            if self.wheels_value > max:
                self.wheels_value = max
            elif self.wheels_value < min:
                self.wheels_value = min
        elif move == "right":
            self.turn_value -= inc1
            if self.turn_value > max:  # Checks if head has reached farthest lef value
                self.turn_value = max
            elif self.turn_value < min:  # Checks if head is in the farthest right postion
                self.turn_value = min
        elif move == "left":
            self.turn_value += inc1
            if self.turn_value > max:  # Checks if head has reached farthest left value
                self.turn_value = max
            elif self.turn_value < min:  # Checks if head is in the farthest right postion
                self.turn_value = min

        moves[move].__call__()


threading.Thread(target=FaceDetection).start()
