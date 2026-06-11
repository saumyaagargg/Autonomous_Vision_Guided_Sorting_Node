# Autonomous Vision-Guided Sorting Node

## Overview

This project explores a dual-layer architecture for automated object sorting, combining computer vision (MPU layer) with embedded sorting logic (MCU layer). The goal is to detect objects in real time using YOLOv8 and trigger corresponding bin-sorting commands on an ESP32 microcontroller.

> **Development Note:** This project is currently developed and validated entirely in software. The MPU layer runs on a Windows laptop (in place of a Raspberry Pi), using a webcam for live object detection. The MCU layer runs in the Wokwi ESP32 simulator (in place of physical ESP32 hardware). No physical Raspberry Pi or ESP32 has been used yet.

---

## System Architecture

### Original Design (Target Architecture)

```text
Camera
  │
  ▼
MPU Layer (Python + YOLOv8)
  │
  ▼
Object Classification
  │
  ▼
UART Communication
  │
  ▼
MCU Layer (ESP32)
  │
  ▼
Sorting Action
```

### Current Implementation (Software-Validated)

```text
MPU Layer (Windows Laptop)
----------------------------------------
Webcam
↓
OpenCV Frame Capture
↓
YOLOv8 Detection
↓
Class Labels

UART Communication (Planned)

MCU Layer (Wokwi ESP32 Simulator)
----------------------------------------
Serial Input
↓
Sorting Logic
↓
CMD: ACTUATE_BIN_X
```

The two layers have been developed and tested independently. Direct runtime serial integration between them is the next planned step.

---

## Technologies Used

* Python 3.14
* OpenCV
* Ultralytics YOLOv8 (Nano)
* ESP32 (Arduino C++ Framework)
* Wokwi ESP32 Simulator
* Git
* GitHub

---

## Repository Structure

```text
Autonomous_Vision_Guided_Sorting_Node/
├── mpu/
│   ├── detect.py        # YOLOv8 object detection script
│   └── yolov8n.pt       # YOLOv8 Nano model weights
├── mcu/
│   └── main.ino         # ESP32 sorting logic (Wokwi-tested)
├── README.md
└── .gitignore
```

---

## MPU Layer — Object Detection

**Hardware Used:** Windows laptop with webcam (used as a functional substitute for Raspberry Pi hardware)

### Functionality (`detect.py`)

1. Initializes webcam feed
2. Captures frames continuously
3. Runs real-time YOLOv8 inference
4. Renders bounding boxes and class labels
5. Logs detected objects

### Detection Pipeline

```text
Webcam
↓
OpenCV Frame Capture
↓
YOLOv8 Nano Model
↓
Object Classification
↓
Detection Output
```

### Verified Detections Observed During Testing

* Person
* Chair
* Book
* Cup
* Bottle

### Running the Detection Script

```bash
pip install ultralytics opencv-python
python mpu/detect.py
```

---

## MCU Layer — Sorting Logic

**Hardware Used:** ESP32 (simulated via Wokwi — no physical board yet)

### Functionality (`main.ino`)

1. Initializes serial communication (115200 baud)
2. Receives object label strings
3. Parses object tokens
4. Executes corresponding sorting commands

### Sorting Map

| Object | Action | Command       |
| ------ | ------ | ------------- |
| bottle | Bin 1  | ACTUATE_BIN_1 |
| cup    | Bin 2  | ACTUATE_BIN_2 |
| book   | Bin 3  | ACTUATE_BIN_3 |

### Example Wokwi Output

```text
Received: bottle
CMD: ACTUATE_BIN_1

Received: cup
CMD: ACTUATE_BIN_2

Received: book
CMD: ACTUATE_BIN_3
```

---

## Communication Design

### Protocol

UART Serial Communication

### Configuration

* Baud Rate: 115200
* Data Format: ASCII Strings
* Packet Terminator: Newline (`\n`)

### Packet Examples

```text
bottle\n  →  CMD: ACTUATE_BIN_1
cup\n     →  CMD: ACTUATE_BIN_2
book\n    →  CMD: ACTUATE_BIN_3
```

### Intended Runtime Flow

```text
MPU detects bottle
↓
Transmit: bottle\n
↓
MCU receives bottle
↓
Execute: ACTUATE_BIN_1
```

The communication protocol has been designed and validated on the MCU side. The MPU side (`detect.py`) does not yet transmit over a live serial connection to the MCU because the MCU currently operates inside the Wokwi simulation environment rather than on physical ESP32 hardware.

---

## Project Status

### Completed

* Python environment setup
* YOLOv8 installation and configuration
* OpenCV integration
* Webcam-based object detection
* ESP32 firmware development
* Wokwi simulation setup
* Serial command processing
* Sorting decision logic
* Git version control setup
* GitHub repository deployment

### Currently Validated

* Real-time object detection
* ESP32 sorting logic
* Wokwi simulation workflow
* UART protocol design
* Independent MPU and MCU module testing

### Not Yet Implemented

* Physical ESP32 hardware deployment
* Direct MPU-to-MCU runtime communication
* Servo motor actuation
* Conveyor-based sorting mechanism
* Custom-trained object classification dataset

---

## Future Extensions

Potential future improvements include:

* Physical ESP32 deployment
* Servo-driven sorting bins
* Conveyor belt integration
* Custom-trained YOLO model for waste classification
* End-to-end autonomous sorting workflow

---

## Engineering Significance

This project demonstrates the separation of AI inference and deterministic control using an MPU–MCU co-architecture.

Key engineering areas explored:

* Computer Vision
* Object Detection
* Embedded Systems
* ESP32 Firmware Development
* Serial Communication
* MPU–MCU System Design
* Simulation-Based Validation
* Git-Based Development Workflow

---

## Repository

https://github.com/saumyaagargg/Autonomous_Vision_Guided_Sorting_Node
