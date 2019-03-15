import cv2
import numpy as np

class CoordinateStore:

    def __init__(self):

        self.points = []
        self.mins = np.zeros(3)
        self.maxs = np.zeros(3)

    def getPixelFromMouseClick(self,evt,x,y,flags,pic):
        ("mouse worked")
        if evt == cv2.EVENT_LBUTTONDOWN:
            print(x,y)
            self.points.append((x,y))

    def getMinHue(self, value):
        self.mins[0] = value

    def getMinSat(self,value):
        self.mins[1] = value

    def getMinVal(self,value):
        self.mins[2] = value

    def getMaxHue(self,value):
        self.maxs[0] = value

    def getMaxSat(self,value):
        self.maxs[1] = value

    def getMaxVal(self,value):
        self.maxs[2] = value

def main():
    coordinateStore = CoordinateStore()

    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Orignal", cv2.WINDOW_NORMAL)
    cv2.namedWindow("HSV", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)

    # using sliders, create scalars for min and max value you want to track
    # a scalar will be a numpy array (np.array) that takes in 3 values, minH, minS, minV. then create second scalar for other 3 max values
    # create 6 trackbars, createTrackBar with callback methods to set your six variables
    cv2.createTrackbar('minHue', 'HSV', 0, 255, coordinateStore.getMinHue)
    cv2.createTrackbar('maxHue', 'HSV', 0, 255, coordinateStore.getMaxHue)
    cv2.createTrackbar('minSat', 'HSV', 0, 255, coordinateStore.getMinSat)
    cv2.createTrackbar('maxSat', 'HSV', 0, 255, coordinateStore.getMaxSat)
    cv2.createTrackbar('minVal', 'HSV', 0, 255, coordinateStore.getMinVal)
    cv2.createTrackbar('maxVal', 'HSV', 0, 255, coordinateStore.getMaxVal)

    cv2.setMouseCallback("HSV", coordinateStore.getPixelFromMouseClick)

    while (1):

        status,img = cap.read()

        # display original
        cv2.imshow("Original", img)

        # built in function for BGR to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # display transformmed image
        cv2.imshow("HSV", hsv)

        # create object tracker
        # use openCV inRange method to find the values between the scalars from HSV image and the result will go grayscale
        # make it a binary image, white/black
        mask = cv2.inRange(hsv, coordinateStore.mins, coordinateStore.maxs)

        kernel = np.ones((5,5),np.uint8)

        # dilate, erode the grayscale image to get better representation
        #dialate function
        dilate = cv2.dilate(mask,kernel,iterations = 1)
        #erode function
        erode = cv2.erode(dilate,kernel,iterations = 1)

        cv2.imshow("Mask", mask)

        cv2.resizeWindow("Original", 500,500)
        cv2.resizeWindow("HSV", 500,500)
        cv2.resizeWindow("Mask", 500,500)

        k = cv2.waitKey(20)
        if k == 27:
            break

    cv2.destroyAllWindows()

    print ("Selected Coordinates: ")
    for i in coordinateStore.points:
        print (hsv[i])

main()
