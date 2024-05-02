import cv2
import numpy as np
import time, datetime
import logging
import logging.config
from os import path

log_file_path = path.join(path.dirname(path.abspath(__name__)), 'logger.config')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("Engine")

__max = {
    0: 0,
    1: 0,
    2: 0
}


def get_max_pixel(ip_address, username, password, profile, frames):
    cap = cv2.VideoCapture('rtsp://' +
                           username + ':' +
                           password +
                           '@' + ip_address + '/axis-media/media.amp' + '?streamprofile=' + profile)
    if cap is None or not cap.isOpened():
        logging.error('Warning: unable to open video source: ', ip_address)
        return None
    frames_count = 0
    while frames_count < frames:
        ret, frame = cap.read()
        # Rechteck auf Bild zeichnen (zur Entwicklung)
        cv2.rectangle(frame, (360, 280), (640, 490), (0, 255, 0), 3)
        roi = frame[280:490, 360:640]

        # Calculate the average color of the ROI
        average_color = np.mean(roi, axis=(0, 1))

        if (average_color[0] > __max[0]):
            __max[0] = average_color[0]
        if (average_color[1] > __max[1]):
            __max[1] = average_color[1]
        if (average_color[2] > __max[2]):
            __max[2] = average_color[2]
        logging.debug("Max color: " + str(__max))
        # cv2.imshow('frame',frame)
        frames_count = frames_count + 1
        logging.debug("Frames count: " + str(frames_count))
        if not ret:
            logging.error('Warning: unable to read next frame')
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return __max


def open_camera_profile(ip_address, username, password, profile, maxcolor):  # Open the camera
    cap = cv2.VideoCapture('rtsp://' +
                           username + ':' +
                           password +
                           '@' + ip_address + '/axis-media/media.amp' + '?streamprofile=' + profile)
    if cap is None or not cap.isOpened():
        logging.error('Warning: unable to open video source: ', ip_address)
        return None
    while True:
        ret, frame = cap.read()
        # Rechteck auf Bild zeichnen (zur Entwicklung)
        cv2.rectangle(frame, (360, 280), (640, 490), (0, 255, 0), 3)
        roi = frame[280:490, 360:640]

        # Calculate the average color of the ROI
        average_color = np.mean(roi, axis=(0, 1))

        # If you want to convert the average color to RGB format
        if ((average_color[0] > round(maxcolor[0] - 2, 1)) & (average_color[1] > round(maxcolor[1] - 2, 1)) & (
                average_color[2] > round(maxcolor[2] - 2, 1))):
            cap.release()
            return True
        logging.debug("Waiting for camera position")
        # Zur Entwicklung: Frame anzeigen
        #cv2.imshow('frame', frame)

        if not ret:
            logging.error('Warning: unable to read next frame')
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def writeScreenshot(ip_address, username, password, profile, screenshot):
    # Open the camera
    cap = cv2.VideoCapture('rtsp://' +
                           username + ':' +
                           password +
                           '@' + ip_address + '/axis-media/media.amp' + '?streamprofile=' + profile)
    if cap is None or not cap.isOpened():
        logging.error('Warning: unable to open video source: ', ip_address)
        return None
    ret, frame = cap.read()

    cv2.imwrite(str(screenshot)+ ".png", frame)
    cv2.destroyAllWindows()
    logging.info(str(screenshot) + ".png erstellt.")
