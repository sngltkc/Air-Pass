# Air-Pass

### An Offline AIoT Edge Gateway for Smart Access Control

Air-Pass is an offline AIoT-based smart access control system that combines face detection and hand gesture recognition to provide a gesture-based authentication mechanism.

The system processes visual input locally, without requiring an internet connection or cloud-based processing. It integrates computer vision techniques with a microcontroller-based physical access control mechanism.

## Features

- **Face Detection:** Detects human faces using OpenCV and Haar Cascade.
- **Hand Gesture Recognition:** Uses MediaPipe Hands to detect and classify hand gestures.
- **Gesture-Based Authentication:** Implements a predefined gesture sequence (`PEACE → FIST`) as an authentication mechanism.
- **Offline Processing:** Performs visual processing locally without cloud connectivity.
- **Hardware Integration:** Communicates with an Arduino over serial communication.
- **Physical Access Control:** Controls a servo motor, status LEDs, and an OLED display.
- **Performance Monitoring:** Tracks frame processing latency and FPS.

## System Architecture

The system consists of two main components:

1. **Edge Processing Unit:** Runs the Python application and handles face detection, hand tracking, gesture recognition, and authentication.
2. **Microcontroller Unit:** Receives serial commands and controls the physical locking mechanism.

### Technologies Used

| Component            | Technology           |
| -------------------- | -------------------- |
| Programming Language | Python, C++          |
| Face Detection       | OpenCV, Haar Cascade |
| Hand Tracking        | MediaPipe            |
| Serial Communication | PySerial             |
| Microcontroller      | Arduino              |
| Actuation            | Servo Motor          |
| Visual Feedback      | OLED Display, LEDs   |

## Project Structure

```text
Air-Pass/
├── airpass_main.py
├── arduino/
│   └── airpass_controller.ino
├── older/
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python
- OpenCV
- MediaPipe
- PySerial
- Arduino-compatible microcontroller
- Webcam
- Servo motor
- OLED display
- Status LEDs

## Installation

Clone the repository:

```bash
git clone https://github.com/sngltkc/Air-Pass.git
cd Air-Pass
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux:**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Before running the application, make sure to:

- Connect the Arduino to the computer.
- Configure the serial port in `airpass_main.py` according to your environment.
- Connect the webcam.
- Upload the Arduino controller sketch.
- Verify the servo, LEDs, and OLED display connections.

## Running the Application

```bash
python airpass_main.py
```

Press `q` to exit the application.

## Performance Monitoring

The application displays:

- Average frame processing latency (ms)
- Current FPS
- Gesture recognition status
- Authentication sequence
- Access control status

## Project Status

Developed as an AIoT-based smart access control project. Further improvements and documentation may be added.

## License

No license has been assigned yet. All rights reserved unless otherwise stated.
