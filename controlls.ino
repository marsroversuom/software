void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT); // onboard LED for testing
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    if (command == '1') {
      digitalWrite(13, HIGH); // Turn LED on
    } else if (command == '0') {
      digitalWrite(13, LOW);  // Turn LED off
    }
  }
}
