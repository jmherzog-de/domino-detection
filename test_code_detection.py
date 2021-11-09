
# !!!!!  QUIT BY TYPING "q"  !!!!!

# Future Version: detect and warp turned stones
# - detect biggest circle (which does not match the mean value of the other circles)
# - warp perspective on that circle
# - do the counting part as done with the straight stones

import cv2
import numpy as np


def emptyCallback(arg):
    pass


def getContours(in_img, out_img):
##    circle_vals = []
##    circle_coords = []
##    circle_corners = []

    _, contours, hierarchy = cv2.findContours(in_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:                                              # get rid of small errors --> could get rid of points if too small
            cv2.drawContours(out_img, cnt, -1, (255,0,255), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)         # number of conerpoints

            objCorner = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            if objCorner == 4:  objectType = 'Rect'
            elif objCorner >4 :
                objectType = 'Circle'

##                # ---- for future versions -----------
##                # build mean of all circles
##                circle_vals.append(area)
##                circle_coords.append(approx)
##                circle_corners.append(objCorner)
##                # ------------------------------------
                
            else:   objectType = 'None'

            cv2.rectangle(imgContour, (x,y), (x+w,y+h), (255,0,0), 2)
            cv2.putText(imgContour, objectType, (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0))



##    # ----------------------------------------------- for future versions -------------------------------------------------------------
##    # build mean of all circles
##    circle_mean = 0
##
##    for val in circle_vals:
##        circle_mean += val
##
##    circle_mean = circle_mean / len(circle_vals)
##
##    print(circle_mean)
##
##    x_list = []
##    y_list = []
##    x_new = []
##    y_new = []
##    x_to_pop = []
##    y_to_pop = []
##
##    for i in range(len(circle_vals)):
##        if circle_vals[i] > (circle_mean + 200):            # 200 (random) threshold
##            print(circle_vals[i])
##            print(circle_coords[i])
##            contour_corners = circle_coords[i]
##            for i in range(len(contour_corners)):
##                cv2.putText(imgContour, str(i), (contour_corners[i][0][0],contour_corners[i][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))
##
##                x_list.append(contour_corners[i][0][0])
##                y_list.append(contour_corners[i][0][1])
##
##            # ++++ from here on only bad things happen +++++++++++++
##            for i in range(len(x_list)):
##                if x_list[i] > (x_list[0] + 20) or x_list[i] < (x_list[0] - 20):         # 20 = really bad threshold only for testing purposes
##                    x_to_pop.append(i)
###                    x_new.append(x_list.pop(i))
##
##            for i in range(len(y_list)):
##                if y_list[i] > (y_list[0] + 20) or y_list[i] < (y_list[0] - 20):         # 20 = really bad threshold only for testing purposes
##                    y_to_pop.append(i)
###                    y_new.append(y_list.pop(i))
##
##            for i in range(len(x_to_pop)):
##                x_new.append(x_list.pop(x_to_pop[i]-i*1))
##
##            for i in range(len(y_to_pop)):
##                y_new.append(y_list.pop(y_to_pop[i]-i*1))
##
##            x_list.clear()
##            y_list.clear()
##            x_new.clear()
##            y_new.clear()
##
##            cv2.rectangle(imgContour, (x,y), (x+w,y+h), (0,255,0), 4)  # kind of buggy but not important so i wont fix it right now
##            print(circle_corners[i])
##
##    circle_vals.clear()
##    circle_coords.clear()
##    circle_corners.clear()
##    # ----------------------------------------------------------------------------------------------------------------------------------------------






kernel = np.ones((5,5), np.uint8)

cv2.namedWindow("LeWindow")
cv2.resizeWindow("LeWindow", 1440, 950)
cv2.createTrackbar("Thresh_1", "LeWindow", 90, 255, emptyCallback)
cv2.createTrackbar("Thresh_2", "LeWindow", 120, 255, emptyCallback)

#img = cv2.imread('images/shapes.png')     # 30 and 30
#img = cv2.imread('images/6.jpeg')       # 90 and 160            90 and 120 for small errors
img = cv2.imread('images/3.jpeg')
#img = cv2.imread('images/1.jpeg')
#img = cv2.imread('images/1_1.jpeg')     # use 160 and 255 in canny

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
#imgBlur = cv2.GaussianBlur(imgHSV, (7,7), 1)


while True:
    Thr_1 = cv2.getTrackbarPos("Thresh_1", "LeWindow")
    Thr_2 = cv2.getTrackbarPos("Thresh_2", "LeWindow")


    imgCanny = cv2.Canny(imgBlur, Thr_1, Thr_2)
    imgDilation = cv2.dilate(imgCanny, kernel, iterations=1)

    imgContour = img.copy()
    getContours(imgDilation, imgContour)


    cv2.imshow('LeWindow', imgContour)
    cv2.imshow('Blur', imgBlur)
    cv2.imshow('Canny', imgCanny)
    cv2.imshow('Dilation', imgDilation)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
