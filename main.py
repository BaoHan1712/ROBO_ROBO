import cv2
from ultralytics import YOLO
import numpy as np
from utils import  offset_backboard

cap = cv2.VideoCapture("data\clip_7d.mp4")

class_name = ['backboard', 'ball', 'basket']

model = YOLO("model\yolo11.onnx")

#fps
prev_frame_time = 0
new_frame_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    new_frame_time = cv2.getTickCount()

    frame = cv2.resize(frame, (1080, 720))
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # contour(frame,hsv)

    results = model.predict(source=frame, imgsz=320, conf=0.65)

    for result in results:
        boxes = result.boxes 
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  
            cls = int(box.cls[0])

            if cls == 0 or cls == 2 or cls == 1:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                label = f'{class_name[cls]}'
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            if cls == 0 :
                w = x2 - x1
                h = y2 - y1
                cx, cy = x1 + w // 2, y1 + h // 2

                # Vẽ đường tròn ở giữa bbox
                cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)

                #Gọi hàm offset
                offset = offset_backboard(frame,cx)

                # In độ lệch so với trục trung tâm
                if offset < -2:
                    cv2.putText(frame, f'Lech trai: {abs(offset)} px', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                elif offset > 2:
                    cv2.putText(frame, f'Lech phai: {abs(offset)} px', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    fps = cv2.getTickFrequency() / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    fps_text = f'FPS: {int(fps)}'
    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    cv2.imshow('Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
