from ultralytics import YOLO
import cv2
import time

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Open webcam
camera = cv2.VideoCapture(0)

# Classes used by sorting system
TARGET_CLASSES = {"bottle", "cup", "book"}

# Debounce variables
last_sent = None
last_sent_time = 0

# Command display
last_command_display = ""

while True:

    success, frame = camera.read()

    if not success:
        break

    # Run YOLO inference
    results = model(frame)

    # Draw YOLO bounding boxes
    annotated_frame = results[0].plot()

    detected_this_frame = False

    # Process detections
    for box in results[0].boxes:

        class_id = int(box.cls[0])
        cls_name = model.names[class_id]

        if cls_name in TARGET_CLASSES:

            detected_this_frame = True

            # Sorting logic
            if cls_name == "bottle":
                command = "ACTUATE_BIN_1"

            elif cls_name == "cup":
                command = "ACTUATE_BIN_2"

            elif cls_name == "book":
                command = "ACTUATE_BIN_3"

            else:
                continue

            # Keep command visible while object exists
            last_command_display = command

            now = time.time()

            # Debounce command generation
            if cls_name != last_sent or (now - last_sent_time) > 2:

                print(f"\nDetected: {cls_name}")
                print(f"Command: {command}")

                # NOTE:
                # In physical deployment this command would be sent
                # to the ESP32 through UART serial communication:
                #
                # ser.write(f"{cls_name}\\n".encode())
                #
                # Current project validates MPU (YOLOv8)
                # and MCU (ESP32/Wokwi) layers independently.

                last_sent = cls_name
                last_sent_time = now

    # Clear command if no sortable object is visible
    if not detected_this_frame:
        last_command_display = ""

    # Display command on screen
    if last_command_display:

        cv2.putText(
            annotated_frame,
            last_command_display,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("AI MPU Layer", annotated_frame)

    # ESC key exits program
    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()