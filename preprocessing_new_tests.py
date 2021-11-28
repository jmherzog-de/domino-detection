import cv2
import numpy as np

cap = cv2.VideoCapture(2)       # id of the webcam
kernel = np.ones((5,5), np.uint8)
kernel_3 = np.ones((3,3), np.uint8)





def boundingBoxStone(x, y, w, h):
    # find orientation of stone
    # w > h equals upright
    x_new = 0
    y_new = 0
    h_new = 0
    w_new = 0
    x_2 = 0             # predefined to catch errors
    y_2 = 0
    h_half = 0
    w_half = 0
    if w > h:
        id = 1
        # for h the percentage of the stone = 4,8
        # for w the percentage of the stone = 72,5
        h_new = (h/7) * 100
        w_new = (w/75) * 100
        y_new = y - ((h_new-h)/2)
        x_new = x - ((w_new-w)/2)

        cv2.rectangle(imgContour, (int(x_new),int(y_new)), (int(x_new+w_new),int(y_new+h_new)), (0,255,0), 3)

        # now 2 seperate boxes for the seperate sides:
        # x_new still correct, y now has to be split for 2 boxes
        # y1 stays y_new and y2 has to be recalculated
        y_2 = y + (h/2)
        h_half = h_new/2

        cv2.rectangle(imgContour, (int(x_new),int(y_new)), (int(x_new+w_new),int(y_new+h_half)), (0,0,255), 2)
        cv2.rectangle(imgContour, (int(x_new),int(y_2)), (int(x_new+w_new),int(y_2+h_half)), (0,0,255), 2)

    # h > w equals sideways
    else:
        id = 2
        h_new = (h/75) * 100
        w_new = (w/7) * 100
        y_new = y - ((h_new-h)/2)
        x_new = x - ((w_new-w)/2)

        cv2.rectangle(imgContour, (int(x_new),int(y_new)), (int(x_new+w_new),int(y_new+h_new)), (0,255,0), 3)

        # seperate boxes
        x_2 = x + (w/2)
        w_half = w_new/2

        cv2.rectangle(imgContour, (int(x_new),int(y_new)), (int(x_new+w_half),int(y_new+h_new)), (0,0,255), 2)
        cv2.rectangle(imgContour, (int(x_2),int(y_new)), (int(x_2+w_half),int(y_new+h_new)), (0,0,255), 2)
    
    return int(x_new), int(y_new), int(w_new), int(h_new), int(y_2), int(x_2), int(h_half), int(w_half), id


def insideRect(point, box):
    # return True if given point is inside given rect
    # point has to be (x,y)
    # box has to be (x,y,w,h)
    if (point[0] > box[0] and point[1] > box[1]) and (point[0] < box[0]+box[2] and point[1] < box[1]+box[3]):
        return True
    else:
        return False



def getContours(in_img, out_img):
##    circle_vals = []
##    circle_coords = []
##    circle_corners = []
    circle_centers = []
    stone_boxes = []

    _, contours, hierarchy = cv2.findContours(in_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 700:                                              # get rid of small errors --> could get rid of points if too small
            cv2.drawContours(out_img, cnt, -1, (255,0,255), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)         # number of conerpoints

            objCorner = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            if objCorner == 4 or objCorner == 5:                                      # usually 4, here 5 for small errors
                objectType = 'Rect'
                stone_boxes.append(boundingBoxStone(x, y, w, h))
            elif objCorner > 5:
                objectType = 'Circle'
                # find center of circle
                new_center = [int(x+(w/2)), int(y+(h/2))]
                circle_centers.append(new_center)
                cv2.putText(imgContour, "x", (new_center[0],new_center[1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))

##                # ---- for future versions -----------
##                # build mean of all circles
##                circle_vals.append(area)
##                circle_coords.append(approx)
##                circle_corners.append(objCorner)
##                # ------------------------------------
                
            else:   objectType = 'None'

            cv2.rectangle(imgContour, (x,y), (x+w,y+h), (255,0,0), 2)
            cv2.putText(imgContour, objectType, (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0))

    # ********** check if circle in box ***************************
    circle_count = 0
    for i in range(len(stone_boxes)):
        for j in range(len(circle_centers)):
            if (insideRect(circle_centers[j], stone_boxes[i])):
                circle_count += 1
        cv2.putText(imgContour, str(circle_count), (stone_boxes[i][0], stone_boxes[i][1]-35), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255))
        circle_count = 0    
    
    # ********** check the split boxes ****************************
    # check id to determine orientation
    # !!! inefficient since we go over every circle again, potential to speed up the process !!!
    circle_count_side_1 = 0
    circle_count_side_2 = 0
    id_x = 0
    id_y = 1
    for i in range(len(stone_boxes)):
        for j in range(len(circle_centers)):
            if stone_boxes[i][8] == 1:
                if (insideRect(circle_centers[j], [stone_boxes[i][0], stone_boxes[i][1], stone_boxes[i][2], stone_boxes[i][6]])):
                    circle_count_side_1 += 1
                elif (insideRect(circle_centers[j], [stone_boxes[i][0], stone_boxes[i][4], stone_boxes[i][2], stone_boxes[i][6]])):
                    circle_count_side_2 += 1
                id_x = 0
                id_y = 4

            elif stone_boxes[i][8] == 2:
                if (insideRect(circle_centers[j], [stone_boxes[i][0], stone_boxes[i][1], stone_boxes[i][7], stone_boxes[i][3]])):
                    circle_count_side_1 += 1
                elif (insideRect(circle_centers[j], [stone_boxes[i][5], stone_boxes[i][1], stone_boxes[i][7], stone_boxes[i][3]])):
                    circle_count_side_2 += 1
                id_x = 5
                id_y = 1

        cv2.putText(imgContour, str(circle_count_side_1), (stone_boxes[i][0], stone_boxes[i][1]-10), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255))
        cv2.putText(imgContour, str(circle_count_side_2), (stone_boxes[i][id_x], stone_boxes[i][id_y]-10), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255))
        circle_count_side_1 = 0
        circle_count_side_2 = 0

##    # *********** find appending stones ************
##    findAppending(stone_boxes)
##    
##
##    stone_boxes.clear()
##    circle_centers.clear()










while True:
    ret, frame = cap.read()

    image = np.zeros(frame.shape, np.uint8)

    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, 2)

    frameBlur = cv2.GaussianBlur(frameGray, (7,7), 3)
    frameCanny = cv2.Canny(frameBlur, 50, 160)
    frameDilation = cv2.dilate(frameCanny, kernel, iterations=1)

    # ned schlecht aber kacke bei ungleicher Beleuchtung
    (thresh, blackAndWhiteImage) = cv2.threshold(frameGray, 27, 255, cv2.THRESH_BINARY)
    BaWDilation = cv2.dilate(blackAndWhiteImage, kernel, iterations=1)
    BaWErosion = cv2.erode(blackAndWhiteImage, kernel, iterations=1)

    BaWCanny = cv2.Canny(BaWErosion, 50, 160)

    th1 = cv2.adaptiveThreshold(frameGray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,4)
    th2 = cv2.adaptiveThreshold(frameGray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,4)

    blur = cv2.GaussianBlur(th1,(5,5),2)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    th3Canny = cv2.Canny(th3, 50, 160)
    th3Dilation = cv2.dilate(th3Canny, kernel, iterations=1)

    # harter trash
#    th3Erosion = cv2.erode(th3, kernel_3, iterations=3)
#    th3E_Dilation = cv2.dilate(th3Erosion, kernel_3, iterations=2)

    cv2.imshow('frame', frame)
    cv2.imshow('gray', frameGray)
#    cv2.imshow('blur', frameBlur)
#    cv2.imshow('canny', frameCanny)
#    cv2.imshow('dilation', frameDilation)
    cv2.imshow('B&W', blackAndWhiteImage)
    cv2.imshow('Adap Mean', th1)
    cv2.imshow('Adap Gauss', th2)
    cv2.imshow('Gauss + Otsu', th3)
    cv2.imshow('G+O Canny', th3Canny)
    cv2.imshow('G+O Dilation', th3Dilation)
#    cv2.imshow('G+O Erosion', th3Erosion)
#    cv2.imshow('G+O Dilation', th3E_Dilation)
#    cv2.imshow('B&W Dilation', BaWDilation)
#    cv2.imshow('B&W Erosion', BaWErosion)
#    cv2.imshow('B&W Canny', BaWCanny)




    imgContour = frame.copy()
    getContours(th3Dilation, imgContour)


    cv2.imshow('Contour', imgContour)






    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()