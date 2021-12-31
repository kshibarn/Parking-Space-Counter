import cv2
import pickle
import cvzone
import numpy as np

with open('ParkPos', 'rb') as f:  # Read Pickle File
    posList = pickle.load(f)

# Show Video
show = cv2.VideoCapture('carPark.mp4')

width, height = 108, 47


def checkParkingSpace(imgProc):

    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgProc[y: y + height, x: x + width]
        # cv2.imshow(str(x * y), imgCrop)  Also showing specific marked car boundaries

        count = cv2.countNonZero(imgCrop)  # Counting Values

        if count < 850:
            color = (14, 199, 94)
            thickness = 4
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color,
                      thickness)  # Removed boundaries for specific cars
        cvzone.putTextRect(img, str(count), (x, y + height - 4), scale=1, thickness=2,
                           offset=0, colorR=color)  # Putting Values inside box

        cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(118, 206, 214))


while True:

    if show.get(cv2.CAP_PROP_POS_FRAMES) == show.get(cv2.CAP_PROP_FRAME_COUNT):  # For Looping the Video
        show.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Resetting Video

    success, img = show.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 27, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    # imgMedian1 = cv2.medianBlur(imgThreshold, 7)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThresh", imgMedian)
    # cv2.imshow("ImageThreshold", imgMedian1)
    cv2.waitKey(8)
