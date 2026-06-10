from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()

    if not success:
        break

    results = model(frame)

    annotated_frame = results[0].plot()

    cv2.imshow("AI MPU Layer", annotated_frame)

    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()