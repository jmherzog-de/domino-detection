import cv2
import numpy as np

# - detect biggest circle (which does not match the mean value of the other circles)
# - warp perspective on that circle
# - count shit


def emptyCallback(arg):
    pass


def getContours(in_img, out_img):
    circle_vals = []
    circle_coords = []
    circle_corners = []

    _, contours, hierarchy = cv2.findContours(in_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
#        print(area)

#        if area > 1100:                                             # clear the induced small errors (90 and 120 for 6.jpeg) --> should be automated in the future 
        if area > 100:
#            print(area)
            cv2.drawContours(out_img, cnt, -1, (255,0,255), 3)

            peri = cv2.arcLength(cnt, True)
#            print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)         # number of conerpoints
#            print(len(approx))                                      # according to number we can make asumptions

            objCorner = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            if objCorner == 4:  objectType = 'Rect'
            elif objCorner >4 :
                objectType = 'Circle'
#                print(area)
                # build mean of all circles
                circle_vals.append(area)
#                circle_coords.append(cv2.boundingRect(approx))
                circle_coords.append(approx)
                circle_corners.append(objCorner)
            else:   objectType = 'None'

            cv2.rectangle(imgContour, (x,y), (x+w,y+h), (255,0,0), 2)
            cv2.putText(imgContour, objectType, (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0))
        
    # build mean of all circles
#    print(circle_vals)
#    print(len(circle_vals))
    circle_mean = 0

    for val in circle_vals:
        circle_mean += val

    circle_mean = circle_mean / len(circle_vals)

    print(circle_mean)

    x_list = []
    y_list = []
    x_new = []
    y_new = []
    x_to_pop = []
    y_to_pop = []

    for i in range(len(circle_vals)):
        if circle_vals[i] > (circle_mean + 200):            # 200 (random) threshhold
            print(circle_vals[i])
            print(circle_coords[i])
#            x, y, w, h = circle_coords[i]
            contour_corners = circle_coords[i]
            for i in range(len(contour_corners)):
#                print(contour_corners[i][0])
#                print(contour_corners[i][0][0])
                cv2.putText(imgContour, str(i), (contour_corners[i][0][0],contour_corners[i][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))

                # ganz böser shit pt.1 wird ab hier getan (remove 5th point)
                x_list.append(contour_corners[i][0][0])
                y_list.append(contour_corners[i][0][1])

            # ganz böser shit pt.2
#            x_list.sort()
#            y_list.sort()

            print(x_list)
            print(y_list)

            # ACHTUNG HARTER BULLSHIT AB HIER, ICH WAR MÜDE

            for i in range(len(x_list)):
                if x_list[i] > (x_list[0] + 20) or x_list[i] < (x_list[0] - 20):         # 20 = ganz mies ungenauer threshhold der alles bumsen kann
                    x_to_pop.append(i)
#                    x_new.append(x_list.pop(i))

            for i in range(len(y_list)):
                if y_list[i] > (y_list[0] + 20) or y_list[i] < (y_list[0] - 20):         # 20 = ganz mies ungenauer threshhold der alles bumsen kann
                    y_to_pop.append(i)
#                    y_new.append(y_list.pop(i))

            for i in range(len(x_to_pop)):
                x_new.append(x_list.pop(x_to_pop[i]-i*1))

            for i in range(len(y_to_pop)):
                y_new.append(y_list.pop(y_to_pop[i]-i*1))


            print(x_new)
            print(y_new)

            x_list.clear()
            y_list.clear()
            x_new.clear()
            y_new.clear()


            cv2.rectangle(imgContour, (x,y), (x+w,y+h), (0,255,0), 4)  # kind of buggy but not important so i wont fix it right now
            print(circle_corners[i])

    circle_vals.clear()
    circle_coords.clear()
    circle_corners.clear()




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



##img = cv2.imread('images/shapes.png', cv2.IMREAD_COLOR)
##
##grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
##cv2.imshow('greyscale', grey)
##
##(_, thresh) = cv2.threshold(grey, 255, 1, 254)
##cv2.imshow('thresholded', thresh)
##
##Canny = cv2.Canny(grey, 50, 50)
##
##
###Get shape contours
##(contours, hierarchy, test) = cv2.findContours(Canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
##thresh_copy = cv2.cvtColor(Canny, cv2.COLOR_GRAY2RGB)
##cv2.drawContours(thresh_copy, contours, contourIdx=-1, color=(0, 255, 0), thickness=2)
##print('number of sides per shape:')
##for contour in contours:
##    print('', contour.shape[0])
##print()
##cv2.imshow('contours', thresh_copy)
##
##
##cv2.waitKey(0)




















#----------- OLD -----------------------------------------------------------------

###img = cv2.imread("images/1_1.jpeg")
###img = cv2.imread("images/6.jpeg")
##img = cv2.imread("images/shapes.png")
##
##
##imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
##imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
##imgCanny = cv2.Canny(imgBlur, 50, 50)
##imgContour = img.copy()
##
##
##def getContours(img):
##    contours, hierarchy, test = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
###    print(len(contours))
##    for cnt in contours:
###        print(cnt)
##        area = cv2.contourArea(cnt)
##        print(area)
###        cv2.drawContours(imgContour, cnt, -1, (255,0,0), 3)
##
##
##cv2.imshow("Original", img)
##cv2.imshow("Gray", imgGray)
##cv2.imshow("Blur", imgBlur)
##cv2.imshow("Canny", imgCanny)
##
##getContours(imgCanny)
##
##cv2.waitKey(0)