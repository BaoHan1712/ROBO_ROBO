from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("best.pt")

model.export(format="onnx",half = True, simplify=True, imgsz=320)

# # # Run inference on 'bus.jpg' with arguments
# model.predict(source="data\o.MOV", save=True, imgsz=320, conf=0.5, show = True)