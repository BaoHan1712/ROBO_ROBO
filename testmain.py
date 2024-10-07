import cv2
from ultralytics import YOLO
import numpy as np
from utils import  process_distance, calculator_offset

cap = cv2.VideoCapture("data\clip_3d.mp4")

class_name = ['backboard', 'ball', 'basket']
model = YOLO("model\\yolo11.onnx")

################# Sửa lại thông số trong này  ##############

KNOWN_DISTANCE_BACKBOARD = 50  # Khoảng cách từ camera tới backboard
KNOWN_HEIGHT_BACKBOARD = 70  # Chiều cao của backboard 

KNOWN_DISTANCE_BASKET = 40  # Khoảng cách từ camera tới backboard
KNOWN_HEIGHT_BASKET = 50  # Chiều cao của backboard 


prev_frame_time = 0
new_frame_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    new_frame_time = cv2.getTickCount()
    frame = cv2.resize(frame, (1080, 720))

    results = model.predict(source=frame, imgsz=320, conf=0.65)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])

            if cls == 0 :  
                label = f'{class_name[cls]}'

                process_distance(frame, x1, y1, y2,  KNOWN_HEIGHT_BACKBOARD,KNOWN_DISTANCE_BACKBOARD)

            # Vẽ đường tròn tại trung tâm
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)

            # Tính độ lệch
                calculator_offset(frame , cx , x1 , y2)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            elif cls == 2 :  
                label = f'{class_name[cls]}'

                process_distance(frame, x1, y1, y2,  KNOWN_HEIGHT_BASKET,KNOWN_DISTANCE_BASKET)

            # Vẽ đường tròn tại trung tâm
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)

            # Tính độ lệch
                calculator_offset(frame , cx, x1 , y2 )

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


    fps = cv2.getTickFrequency() / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    fps_text = f'FPS: {int(fps)}'
    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    cv2.imshow('Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
