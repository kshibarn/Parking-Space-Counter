import cv2
import pickle

width, height = 108, 47

try:                                  # To see saved Image after making 'ParkPos' pickle file
    with open('ParkPos', 'rb') as f:  # Read Pickle File
        posList = pickle.load(f)

except:
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:  # Shows Rectangle when clicked left button
        posList.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:  # Deletion of Rectangle
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('ParkPos', 'wb') as f:  # Create Pickle file 'ParkPos'
        pickle.dump(posList, f)


while True:
    img = cv2.imread("CarParkImg.png")

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 204, 102), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)
