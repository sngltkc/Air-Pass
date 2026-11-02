import cv2

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Gray dönüşüm
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Face detect
    faces = face_cascade.detectMultiScale(
        gray,
       scaleFactor=1.2,
    minNeighbors=8,
    minSize=(80, 80)
    )

    # Dikdörtgen çiz
    for (x, y, w, h) in faces:
     if y < 80:
        continue

    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

    cv2.putText(
        frame,
        "FACE DETECTED",
        (x, y-10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )
    # Ekranda göster
    cv2.imshow("AirPass Security System", frame)

    # Q ile çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()