import numpy as np
import cv2
import logging
import logging.config
from os import path

log_file_path = path.join(path.dirname(path.abspath(__name__)), 'logger.config')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("ColorRecognition")

###### Quadrantenerkennung #####
__pos = {
    0: ""
}

def open_camera_profile(ip_address, username, password, profile, screenshotName):  # Open the camera
    cap = cv2.VideoCapture('rtsp://' +
                           username + ':' +
                           password +
                           '@' + ip_address + '/axis-media/media.amp' + '?streamprofile=' + profile)
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', ip_address)
        return None
    lower_white = np.array([126, 170, 107])
    upper_white = np.array([170, 210, 144])

    lower_white_right = np.array([93, 143, 82])
    upper_white_right = np.array([180, 220, 160])
    while True:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # Bottom bottom left
        cv2.rectangle(frame, (570, 450), (610, 490), (0, 255, 0), 3)
        roi_bot_bot_left = frame[450:490, 570:610]
        average_color_bot_bot_left = np.mean(roi_bot_bot_left, axis=(0, 1))

        # Bottom middle left
        cv2.rectangle(frame, (470, 350), (510, 390), (0, 255, 0), 3)
        roi_bot_mid_left = frame[350:390, 470:510]
        average_color_bot_mid_left = np.mean(roi_bot_mid_left, axis=(0, 1))

        # Bottom left left
        cv2.rectangle(frame, (370, 265), (410, 305), (0, 255, 0), 3)
        roi_bot_left_left = frame[265:305, 370:410]
        average_color_bot_left_left = np.mean(roi_bot_left_left, axis=(0, 1))

        # Bottom bottom right
        cv2.rectangle(frame, (640, 450), (680, 490), (0, 255, 0), 3)
        roi_bot_bot_right = frame[450:490, 640:680]
        average_color_bot_bot_right = np.mean(roi_bot_bot_right, axis=(0, 1))

        # Bottom middle right
        cv2.rectangle(frame, (750, 350), (790, 390), (0, 255, 0), 3)
        roi_bot_mid_right = frame[350:390, 750:790]
        average_color_bot_mid_right = np.mean(roi_bot_mid_right, axis=(0, 1))

        # Bottom right right
        cv2.rectangle(frame, (850, 275), (890, 315), (0, 255, 0), 3)
        roi_bot_right_right = frame[275:315, 850:890]
        average_color_bot_right_right = np.mean(roi_bot_right_right, axis=(0, 1))

        # Top middle left
        cv2.rectangle(frame, (480, 150), (520, 190), (0, 255, 0), 3)
        roi_top_mid_left = frame[150:190, 480:520]
        average_color_top_mid_left = np.mean(roi_top_mid_left, axis=(0, 1))

        # Top left left
        cv2.rectangle(frame, (370, 215), (410, 255), (0, 255, 0), 3)
        roi_top_left_left = frame[215:255, 370:410]
        average_color_top_left_left = np.mean(roi_top_left_left, axis=(0, 1))

        # Top middle right
        cv2.rectangle(frame, (750, 150), (790, 190), (0, 255, 0), 3)
        roi_top_mid_right = frame[150:190, 750:790]
        average_color_top_mid_right = np.mean(roi_top_mid_right, axis=(0, 1))

        # Top right right
        cv2.rectangle(frame, (850, 225), (890, 265), (0, 255, 0), 3)
        roi_top_right_right = frame[225:265, 850:890]
        average_color_top_right_right = np.mean(roi_top_right_right, axis=(0, 1))

        if (average_color_bot_bot_left >= lower_white).all() and (average_color_bot_bot_left <= upper_white).all() and (
                average_color_bot_mid_left >= lower_white).all() and (
                average_color_bot_mid_left <= upper_white).all() and (
                average_color_bot_left_left >= lower_white).all() and (
                average_color_bot_left_left <= upper_white).all():
            cap.release()
            __pos[0] = 1
            cv2.imwrite(screenshotName + ".png", frame)
            return True

        if (average_color_bot_bot_right >= lower_white_right).all() and (
                average_color_bot_bot_right <= upper_white_right).all() and (
                average_color_bot_mid_right >= lower_white_right).all() and (
                average_color_bot_mid_right <= upper_white_right).all() and (
                average_color_bot_right_right >= lower_white_right).all() and (
                average_color_bot_right_right <= upper_white_right).all():
            cap.release()
            __pos[0] = 2
            cv2.imwrite(screenshotName + ".png", frame)
            return True

        if (average_color_top_left_left >= lower_white).all() and (
                average_color_top_left_left <= upper_white).all() and (
                average_color_top_mid_left >= lower_white).all() and (
                average_color_top_mid_left <= upper_white).all() and (average_color_bot_left_left <= lower_white).all():
            cap.release()
            __pos[0] = 3
            cv2.imwrite(screenshotName + ".png", frame)
            return True

        if (average_color_top_right_right >= lower_white).all() and (
                average_color_top_right_right <= upper_white).all() and (
                average_color_top_mid_right >= lower_white).all() and (
                average_color_top_mid_right <= upper_white).all():
            cap.release()
            cv2.imwrite(screenshotName + ".png", frame)
            __pos[0] = 4
            return True

        # Zur Entwicklung: Frame anzeigen
        #cv2.imshow('frame', frame)

        if not ret:
            print('Warning: unable to read next frame')
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    # cv2.destroyAllWindows()

def writeScreenshot(ip_address, username, password, profile, screenshotName):
    # Open the camera
    cap = cv2.VideoCapture('rtsp://' +
                           username + ':' +
                           password +
                           '@' + ip_address + '/axis-media/media.amp' + '?streamprofile=' + profile)
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', ip_address)
        return None
    ret, frame = cap.read()

    cv2.imwrite(screenshotName + ".png", frame)
    cv2.destroyAllWindows()
    print(str(screenshotName) + ".png erstellt.")


def getPosPlate():
    return __pos[0]


###### Farbfilter #####
def colorfilter(filename, colorfiltername):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    lower_red = np.array([0, 100, 110])
    upper_red = np.array([345, 255, 255])

    lower_blue = np.array([90, 95, 50])
    upper_blue = np.array([130, 255, 255])

    lower_yellow = np.array([25, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    final_mask = red_mask + blue_mask + yellow_mask
    filter = cv2.bitwise_and(img, img, mask=final_mask)

    gray_image = cv2.cvtColor(filter, cv2.COLOR_BGR2GRAY)  # anpassen
    threshold = 10
    mask_black = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)[1]
    mask_white = cv2.bitwise_not(mask_black)
    img[mask_white == 255] = [255, 255, 255]

    # bilateral = cv2.bilateralFilter(img, 15,100,100) #anpassen
    # plt.imshow(bilateral) # für RaspberryPi Code entfernen
    # plt.show() # für RaspberryPi Code entfernen

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    bilateral = cv2.bilateralFilter(img, 15, 100, 100)
    cv2.imwrite(colorfiltername, bilateral)


###### Farbereknnung #####
__cube = {
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: ""
}


def getColors(screenshotNumber, screenshot):
    frame = cv2.imread(screenshot)
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    lower_red = np.array([130, 150, 140])
    upper_red = np.array([160, 220, 255])

    lower_blue = np.array([3, 170, 130])
    upper_blue = np.array([70, 255, 255])

    lower_yellow = np.array([83, 170, 160])
    upper_yellow = np.array([140, 255, 240])

    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    red_mask = cv2.inRange(hsv, lower_red, upper_red)

    cv2.rectangle(hsv, (575, 275), (625, 325), (255, 255, 255), 3)
    roi_bottom_left = hsv[270:310, 565:630]
    average_color_bottom_left = np.mean(roi_bottom_left, axis=(0, 1))

    cv2.rectangle(hsv, (650, 275), (700, 325), (255, 255, 255), 3)
    roi_bottom_right = hsv[270:310, 660:720]
    average_color_bottom_right = np.mean(roi_bottom_right, axis=(0, 1))

    cv2.rectangle(hsv, (575, 100), (625, 150), (255, 255, 255), 3)
    roi_above_left = hsv[85:120, 575:635]
    average_color_above_left = np.mean(roi_above_left, axis=(0, 1))

    cv2.rectangle(hsv, (650, 100), (700, 150), (255, 255, 255), 3)
    roi_above_right = hsv[85:120, 665:720]
    average_color_above_right = np.mean(roi_above_right, axis=(0, 1))
    print("average_color_bottom_left" + str(average_color_bottom_left))

    if (average_color_bottom_left >= lower_yellow).all() and (average_color_bottom_left <= upper_yellow).all():
        if (screenshotNumber == 1):
            __cube[1] = 'Yellow'
        if (screenshotNumber == 2):
            __cube[2] = 'Yellow'  # Kann weggelassen werden, da bereits SC1 erkann
        if (screenshotNumber == 3):
            __cube[5] = 'Yellow'  # Kann weggelassen werden, da bereits SC2 erkann
    if (average_color_bottom_left >= lower_red).all() and (average_color_bottom_left <= upper_red).all():
        if (screenshotNumber == 1):
            __cube[1] = 'Red'
        if (screenshotNumber == 2):
            __cube[2] = 'Red'  # Kann weggelassen werden, da bereits SC1 erkannt
        if (screenshotNumber == 3):
            __cube[5] = 'Red'  # Kann weggelassen werden, da bereits SC2 erkann
    if (average_color_bottom_left >= lower_blue).all() and (average_color_bottom_left <= upper_blue).all():
        if (screenshotNumber == 1):
            __cube[1] = 'Blue'
        if (screenshotNumber == 2):
            __cube[2] = 'Blue'  # Kann weggelassen werden, da bereits SC1 erkann
        if (screenshotNumber == 3):
            __cube[5] = 'Blue'  # Kann weggelassen werden, da bereits SC2 erkann
    print("average_color_bottom_right" + str(average_color_bottom_right))

    if (average_color_bottom_right >= lower_yellow).all() and (average_color_bottom_right <= upper_yellow).all():
        if (screenshotNumber == 1):
            __cube[2] = 'Yellow'
        if (screenshotNumber == 2):
            __cube[5] = 'Yellow'
        if (screenshotNumber == 3):
            __cube[6] = 'Yellow'
    if (average_color_bottom_right >= lower_red).all() and (average_color_bottom_right <= upper_red).all():
        if (screenshotNumber == 1):
            __cube[2] = 'Red'
        if (screenshotNumber == 2):
            __cube[5] = 'Red'
        if (screenshotNumber == 3):
            __cube[6] = 'Red'
    if (average_color_bottom_right >= lower_blue).all() and (average_color_bottom_right <= upper_blue).all():
        if (screenshotNumber == 1):
            __cube[2] = 'Blue'
        if (screenshotNumber == 2):
            __cube[5] = 'Blue'
        if (screenshotNumber == 3):
            __cube[6] = 'Blue'
    print("average_color_above_left" + str(average_color_above_left))

    if (average_color_above_left >= lower_yellow).all() and (average_color_above_left <= upper_yellow).all():
        if (screenshotNumber == 1):
            __cube[7] = 'Yellow'
        if (screenshotNumber == 2):
            __cube[4] = 'Yellow'
        if (screenshotNumber == 3):
            __cube[3] = 'Yellow'
    if (average_color_above_left >= lower_blue).all() and (average_color_above_left <= upper_blue).all():
        if (screenshotNumber == 1):
            __cube[7] = 'Red'
        if (screenshotNumber == 2):
            __cube[4] = 'Red'
        if (screenshotNumber == 3):
            __cube[3] = 'Red'
    if (average_color_above_left >= lower_red).all() and (average_color_above_left <= upper_red).all():
        if (screenshotNumber == 1):
            __cube[7] = 'Blue'
        if (screenshotNumber == 2):
            __cube[4] = 'Blue'
        if (screenshotNumber == 3):
            __cube[3] = 'Blue'
    print("average_color_above_right" + str(average_color_above_right))

    if (average_color_above_right >= lower_yellow).all() and (average_color_above_right <= upper_yellow).all():
        if (screenshotNumber == 1):
            __cube[8] = 'Yellow'
        if (screenshotNumber == 2):
            __cube[7] = 'Yellow'  # Kann weggelassen werden, da bereits SC1 erkann
        if (screenshotNumber == 3):
            __cube[4] = 'Yellow'  # Kann weggelassen werden, da bereits SC2 erkann
    if (average_color_above_right >= lower_blue).all() and (average_color_above_right <= upper_blue).all():
        if (screenshotNumber == 1):
            __cube[8] = 'Red'
        if (screenshotNumber == 2):
            __cube[7] = 'Red'  # Kann weggelassen werden, da bereits SC1 erkann
        if (screenshotNumber == 3):
            __cube[4] = 'Red'  # Kann weggelassen werden, da bereits SC2 erkann
    if (average_color_above_right >= lower_red).all() and (average_color_above_right <= upper_red).all():
        if (screenshotNumber == 1):
            __cube[8] = 'Blue'
        if (screenshotNumber == 2):
            __cube[7] = 'Blue'  # Kann weggelassen werden, da bereits SC1 erkann
        if (screenshotNumber == 3):
            __cube[4] = 'Blue'  # Kann weggelassen werden, da bereits SC2 erkann
