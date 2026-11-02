import cv2
import mediapipe as mp
import time
import serial # type: ignore

def detect_gesture(hand_landmarks):
    lm = hand_landmarks.landmark

    index_tip = lm[8]
    middle_tip = lm[12]
    ring_tip = lm[16]
    pinky_tip = lm[20]

    index_pip = lm[6]
    middle_pip = lm[10]
    ring_pip = lm[14]
    pinky_pip = lm[18]

    index_open = index_tip.y < index_pip.y
    middle_open = middle_tip.y < middle_pip.y
    ring_open = ring_tip.y < ring_pip.y
    pinky_open = pinky_tip.y < pinky_pip.y

    if index_open and middle_open and not ring_open and not pinky_open:
        return "PEACE"

    if index_open and middle_open and ring_open and pinky_open:
        return "OPEN"

    if not index_open and not middle_open and not ring_open and not pinky_open:
        return "FIST"

    return "UNKNOWN"


face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

PASSWORD = ["PEACE", "FIST"]

entered_sequence = []
last_accepted_gesture = None

candidate_gesture = None
candidate_start_time = 0

STABLE_TIME = 2.0
TIMEOUT = 3
arduino_sent = False
last_input_time = time.time()

access_granted = False
hand_was_present = False
show_denied_until = 0

# Latency tracking setup
frame_latencies = []
gesture_first_seen_time = None

arduino = serial.Serial("COM4", 9600, timeout=1)
time.sleep(2)

cap = cv2.VideoCapture(0)

while True:
    # Start frame timer
    start_frame_time = time.time()

    success, frame = cap.read()

    if not success:
        print("Camera error")
        break

    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=8,
        minSize=(80, 80)
    )

    face_detected = False

    for (x, y, w, h) in faces:
        if y < 80:
            continue

        face_detected = True

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            "FACE DETECTED",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    hand_detected = False
    gesture = "NO HAND"

    if results.multi_hand_landmarks:
        hand_detected = True

        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            gesture = detect_gesture(hand_landmarks)

    current_time = time.time()

    if current_time - last_input_time > TIMEOUT:
        if len(entered_sequence) > 0:
            if entered_sequence == PASSWORD:
                access_granted = True
                show_denied_until = 0
                if not arduino_sent:
                    arduino.write(b'1')
                print("ACCESS GRANTED")
            else:
                print("ACCESS DENIED")
                access_granted = False
                show_denied_until = current_time + 2.0

        entered_sequence = []
        last_accepted_gesture = None
        candidate_gesture = None
        last_input_time = current_time

    if face_detected and gesture in ["PEACE", "FIST", "OPEN"]:
        hand_was_present = True

        if gesture != candidate_gesture:
            candidate_gesture = gesture
            candidate_start_time = current_time
            # Record when the new gesture was first registered by the model
            gesture_first_seen_time = current_time

        elif current_time - candidate_start_time >= STABLE_TIME:

            if gesture != last_accepted_gesture:
                # Calculate true recognition latency from first sight to accepted state
                rec_latency = (current_time - gesture_first_seen_time) * 1000
                entered_sequence.append(gesture)
                last_accepted_gesture = gesture
                last_input_time = current_time

                print(f"Entered: {entered_sequence} | Detection Latency: {rec_latency:.1f} ms (STABLE_TIME threshold: {STABLE_TIME * 1000:.0f} ms)")

    if gesture == "NO HAND" or gesture == "UNKNOWN":
        candidate_gesture = None
        gesture_first_seen_time = None

        if hand_was_present:
            hand_was_present = False 
            
            if len(entered_sequence) > 0:
                if entered_sequence == PASSWORD:
                    access_granted = True
                    show_denied_until = 0  

                    if not arduino_sent:
                        arduino.write(b'1')
                        
                    print("ACCESS GRANTED")
                    entered_sequence = []
                    last_accepted_gesture = None
                else:
                    access_granted = False
                    show_denied_until = current_time + 2.0  
                    entered_sequence = []
                    last_accepted_gesture = None
                    print("ACCESS DENIED")

    cv2.putText(
        frame,
        "GESTURE: " + gesture,
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "SEQ: " + " -> ".join(entered_sequence),
        (20, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    if access_granted:
        cv2.putText(
            frame,
            "ACCESS GRANTED",
            (20, 180),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )

    if face_detected and hand_detected:
        status = "FACE + HAND OK"
        color = (0, 255, 0)
    elif face_detected:
        status = "FACE OK - SHOW HAND"
        color = (0, 255, 255)
    else:
        status = "NO FACE"
        color = (0, 0, 255)

    cv2.putText(
        frame,
        status,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    # Calculate loop processing time
    end_frame_time = time.time()
    loop_time = (end_frame_time - start_frame_time) * 1000
    frame_latencies.append(loop_time)
    
    # Maintain a moving average of the last 30 frames
    if len(frame_latencies) > 30:
        frame_latencies.pop(0)
    avg_loop_latency = sum(frame_latencies) / len(frame_latencies)
    current_fps = 1000 / avg_loop_latency if avg_loop_latency > 0 else 0

    # Draw average processing latency and current FPS on the window
    latency_text = f"Proc Latency: {avg_loop_latency:.1f} ms ({current_fps:.1f} FPS)"
    cv2.putText(
        frame,
        latency_text,
        (20, frame.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 165, 255),
        2
    )

    cv2.imshow("AirPass Main System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()