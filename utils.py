import cv2 
import numpy as np

def contour(frame, hsv):
    MIN_WIDTH = 15  
    MIN_HEIGHT = 15 
    
    lower_blue = np.array([0, 84, 0]) 
    upper_blue = np.array([179, 255, 255])  

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h

        # Tính độ tròn (circularity)
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if perimeter > 0:
            circularity = (4 * np.pi * area) / (perimeter ** 2)
        else:
            circularity = 0

        # Kiểm tra nếu đối tượng có hình dạng gần tròn
        if w > MIN_WIDTH and h > MIN_HEIGHT and 0.9 <= aspect_ratio <= 1.1 and circularity > 0.4:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Ball: {circularity:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


def offset_backboard(frame_2,cx):
# Tính toán trung tâm khung hình
    frame_center_x = frame_2.shape[1] // 2
    cv2.line(frame_2, (frame_center_x, 0), (frame_center_x, frame_2.shape[0]), (255, 0, 0), 1)
    offset = cx - frame_center_x
    return offset
