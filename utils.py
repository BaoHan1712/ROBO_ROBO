import cv2 
import numpy as np


def contour(frame, hsv):
# Ngưỡng để nhận đối tượng
    MIN_WIDTH = 15  
    MIN_HEIGHT = 15 

    lower_blue = np.array([0, 100, 140]) 
    upper_blue = np.array([17, 255, 255])  

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if w > MIN_WIDTH and h > MIN_HEIGHT:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            

def offset_backboard(frame_2,cx):
# Tính toán trung tâm khung hình
    frame_center_x = frame_2.shape[1] // 2
    cv2.line(frame_2, (frame_center_x, 0), (frame_center_x, frame_2.shape[0]), (255, 0, 0), 1)
    offset = cx - frame_center_x
    return offset