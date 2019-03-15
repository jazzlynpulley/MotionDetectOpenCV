import numpy
import cv2

cap = cv2.VideoCapture(0)
cv2.namedWindow("Original",0)

status, img = cap.read()
average = numpy.float32(img)

while(1):

    status, img = cap.read()

    # create blank image that is 32 bit floating point
    get32Bit = numpy.float32(img/255)

    # blur 32 bit
    result = cv2.blur(get32Bit, (5,5))

    # take running averge of last so many images
    cv2.accumulateWeighted(result,average,0.1)

    # convert back to 8 bit
    result = cv2.convertScaleAbs(average)

    # take absolute difference - this calcs per-element absolute difference between two arrays or array and scalar
    result = cv2.absdiff(result,img)

    # covert to grayscale (use built-in function)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    # get threshold of grayscale
    # hunter uses two thresholds, one starts with a small value then did blur then follows up with second threshold with much larger value
    ret1, result = cv2.threshold(result, 10,50, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    result = cv2.blur(result,(5,5))

    ret1, result = cv2.threshold(result, 200,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # returns three vals,
    image, contours, hierarchy = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < 500:
            continue

    # find the width and heights of those blobs that matter
    (x, y, w, h) = cv2.boundingRect(c)

    # draw rectangle around them
    cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 2)

    cv2.imshow("Orignal", img)

    cv2.imshow("Img1", result)

    k = cv2.waitKey(20)
    if k == 27:
        break

cv2.destroyAllWindows()
