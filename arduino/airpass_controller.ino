#include <Servo.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

Servo lockServo;

const int servoPin = 9;
const int greenLed = 6;
const int redLed = 7;

void showMessage(String msg) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 25);
  display.println(msg);
  display.display();
}

void setup() {
  Serial.begin(9600);

  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);

  digitalWrite(greenLed, LOW);
  digitalWrite(redLed, HIGH);

  lockServo.attach(servoPin);
  lockServo.write(0); // locked position

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    while (true);
  }

  showMessage("SYSTEM LOCKED");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == '1') {
      digitalWrite(redLed, LOW);
      digitalWrite(greenLed, HIGH);

      lockServo.write(90); // unlocked
      showMessage("ACCESS GRANTED");

      delay(5000);

      lockServo.write(0); // locked
      digitalWrite(greenLed, LOW);
      digitalWrite(redLed, HIGH);

      showMessage("SYSTEM LOCKED");
    }

    if (command == '0') {
      digitalWrite(greenLed, LOW);
      digitalWrite(redLed, HIGH);
      lockServo.write(0); // locked position
      showMessage("ACCESS DENIED");
      delay(2000);
      showMessage("SYSTEM LOCKED");
    }
  }
}