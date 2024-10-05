import cv2 
import numpy as np

cap = cv2.VideoCapture("data\clip_7d.mp4")

# Ngưỡng để nhận đối tượng to hay nhỏ
MIN_WIDTH = 25
MIN_HEIGHT = 25

def contour(frame, hsv):
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

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (1080, 720))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    contour(frame, hsv)

    cv2.imshow('Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
