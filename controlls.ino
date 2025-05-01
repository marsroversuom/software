// define pins for motors
#define motor_1 8
#define pwm_1 10

#define motor_2 2
#define pwm_2 3

// have a delay between each motor signal because without this it doesn't work
const int delay_ms = 2;

// since unsigned chars also range from 0 to 255 this is perfect to fetch duties for each of the 6 motors
// duty1 is duties[0] and etc
unsigned char duties[6] = {127, 127, 127, 127, 127, 127};

void setup() {
  pinMode(pwm_2, OUTPUT);
  pinMode(pwm_1, OUTPUT);
  pinMode(motor_1, OUTPUT);
  pinMode(motor_2, OUTPUT);
  Serial.begin(9600);
}

// Turning motors is also sort of convoluted, this works, not entirely sure why
// The signals from motor 1 and motor 2 interfere with eachother as they are controlled with the same driver (this shouldn't happen really)
// This is a workaround

// duty ranges from 0 to 255
// 0 turns the motors CW while 255 CCW max speed. To stop use duty=127 or 128.

void turn_motor1(int duty){
  digitalWrite(motor_1, HIGH);
  digitalWrite(motor_2, LOW);
  analogWrite(pwm_1, duty);
  analogWrite(pwm_2, 0);
  delay(delay_ms);
}


void turn_motor2(int duty){
  digitalWrite(motor_1, LOW);
  digitalWrite(motor_2, HIGH);
  analogWrite(pwm_2, duty);
  analogWrite(pwm_1, 0);
  delay(delay_ms);
}

void loop() {
  // Check if there are at least 6 bytes available in the serial buffer
  if (Serial.available() >= 6) {
    // Read 6 bytes and store them into the duties array
    for (int i = 0; i < 6; i++) {
      duties[i] = Serial.read(); // Store each byte into the duties array
    }
  }

  turn_motor1(duties[0]);
  turn_motor2(duties[1]);

}
