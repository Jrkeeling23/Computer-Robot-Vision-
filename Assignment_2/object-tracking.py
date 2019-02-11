import numpy as np
import cv2 as cv
from numpy.distutils.fcompiler import none

image = none
trackbar_values = {'Red Min': 0, 'Red Max': 0, 'Blue Min': 0, 'Blue Max': 0, 'Green Min': 0,
                   'Green Max': 0}  # RBG Min/Max


def show_unfiltered(image):
    cv.namedWindow("Unfiltered video")  # creates unfiltered video from webcam
    cv.moveWindow("Unfiltered video", 0, 20)

    cv.imshow("Unfiltered video", image)  # sHows the unfiltered video


def show_hsv_values(event, x, y, flags, params):  # Method for mouse clicks on HSV image

    if event is cv.EVENT_LBUTTONDOWN:  # Enters if Left button is clicked
        print("HSV value of location x:", x, "y:", y, "Hue:", params[y, x][0],  # Prints location and HSV values
              "Saturation:", params[y, x][1], "Value:", params[y, x][2])


def show_hsv(image):
    param = cv.cvtColor(image, cv.COLOR_BGR2HSV)  # Converts the image from BGR to HSV
    cv.namedWindow("HSV")  # Creatues window for HSV conversion
    cv.moveWindow("HSV", 643, 20)
    cv.imshow("HSV", param)  # Shows the image
    cv.setMouseCallback("HSV", show_hsv_values, param)  # Passes in HSV image during mouse click


def show_cam():
    # Screen capture code provided by Hunter Lloyd https://ecat.montana.edu/d2l/le/content/524639/viewContent/3826523/View
    capture = cv.VideoCapture(0)
    while True:
        status, image = capture.read()  # Reads in the capture
        show_unfiltered(image)
        create_trackbar(image)
        show_hsv(image)

        k = cv.waitKey(1)
        if k == 27:
            break


# TODO Using Sliders create scalers for the min and max values you want to tracka Scalar will be a numpy array (np.array) that takes 3 values for minH, minS, and minV.......then a second scalar to catch the other three Max values create 3 trackbars, createTrackbar with callback methods to set your six variables
# def set_slider_value(position):
#     values[position]


def set_trackbar_values(numpy_array, array_loc, value):
    numpy_array[array_loc] = value


pass


def create_trackbar(image):
    cv.namedWindow("Track Bar")
    cv.moveWindow("Track Bar", 0, 663)

    hue_min = none
    hue_max = none
    saturation_min = none
    saturation_max = none
    value_min = none
    value_max = none
    numpy = np.array([hue_min, hue_max, saturation_min, saturation_max, value_min, value_max])
    max_hue = 180
    max_slider_value = 255
    min_slider_value = 0
    color_titles = ['Hue Min', 'Hue Max', 'Saturation Min', 'Saturation Max', 'Value Min',
                    'Value Max']  # List to loop through and set trackbar values
    cv.createTrackbar('Hue Min', 'Track Bar', min_slider_value, max_hue,
                      set_trackbar_values)
    set_trackbar_values(numpy, 0, cv.getTrackbarPos('Hue Min', 'Track Bar'))

    cv.createTrackbar('Hue Max', 'Track Bar', min_slider_value, max_hue, set_trackbar_values)
    set_trackbar_values(numpy, 0, cv.getTrackbarPos('Hue Max', 'Track Bar'))
    cv.createTrackbar('Saturation Min', 'Track Bar', min_slider_value, max_slider_value,
                      set_trackbar_values)  # TODO add call back value
    set_trackbar_values(numpy, 0, cv.getTrackbarPos('Saturation Min', 'Track Bar'))
    cv.createTrackbar('Saturation Max', 'Track Bar', min_slider_value, max_slider_value,
                      set_trackbar_values)  # TODO add call back value
    set_trackbar_values(numpy, 0, cv.getTrackbarPos('Saturation Max', 'Track Bar'))
    cv.createTrackbar('Value Min', 'Track Bar', min_slider_value, max_slider_value,
                      set_trackbar_values)  # TODO add call back value
    set_trackbar_values(numpy, 0, cv.getTrackbarPos('Value Min', 'Track Bar'))
    cv.createTrackbar('Value Max', 'Track Bar', min_slider_value, max_slider_value,
                      set_trackbar_values)
    set_trackbar_values(numpy, 0, cv.getTrackbarPos('Value Max', 'Track Bar'))


# TODO Us the OpenCV inRange method to find the values between the scalars from HSV image and the result will go to a grayscale image (make it a binary image, white/black).

# TODO Dilate, erode the grayscale image to get a better representation of the object you are tracking.

# TODO Display the original image and the binary image where everything is black except for the object you are tracking. The tracked object will be white.


show_cam()
cv.destroyAllWindows()
