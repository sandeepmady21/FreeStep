/**
 * ElderStep Pro (FreeStep v2) - Core Safety & Control Firmware
 * Target MCU: ESP32 / ESP32-S3
 *
 * Implements:
 *  1. Fail-Safe "Dead-Man's" Auto-Braking on Rear BLDC Hub Motors
 *  2. Synchronized Dual Vertical Linear Actuator Control with S-Curve Soft Start
 *  3. Anti-Tip Software Interlock between Width-Morphing Actuator & Seat Height
 *  4. 6-Axis IMU (MPU6050) Stumble / Tilt Spike Detection -> Instant Electromagnetic Lock
 *  5. Partial-Weight-Bearing (PWB) Ankle Offloading Coach Indicator
 */

#include <Arduino.h>
#include <Wire.h>

// --- Pin Definitions ---
// Forearm Grip Force Sensors (FSRs)
constexpr int PIN_FSR_LEFT          = 34;
constexpr int PIN_FSR_RIGHT         = 35;

// Vertical Lift Linear Actuators (Left & Right BTS7960 H-Bridges)
constexpr int PIN_LIFT_L_RPWM       = 25;
constexpr int PIN_LIFT_L_LPWM       = 26;
constexpr int PIN_LIFT_R_RPWM       = 27;
constexpr int PIN_LIFT_R_LPWM       = 14;
constexpr int PIN_LIFT_L_HALL       = 18;
constexpr int PIN_LIFT_R_HALL       = 19;

// Horizontal Width-Morphing Actuator ("Bathroom Squeeze Mode")
constexpr int PIN_WIDTH_RPWM        = 32;
constexpr int PIN_WIDTH_LPWM        = 33;
constexpr int PIN_LIMIT_WIDE        = 4;   // 620 mm wide stance confirmed
constexpr int PIN_LIMIT_NARROW      = 5;   // 490 mm bathroom squeeze confirmed

// Rear BLDC Hub Motors (Brake & Throttle PWM)
constexpr int PIN_HUB_BRAKE_EN      = 23;  // HIGH = Electromagnetic Lock Engaged
constexpr int PIN_HUB_THROTTLE_PWM  = 13;

// Cockpit Buttons & Status LEDs
constexpr int PIN_BTN_LIFT_UP       = 16;
constexpr int PIN_BTN_LIFT_DOWN     = 17;
constexpr int PIN_BTN_SQUEEZE_MODE  = 21;
constexpr int PIN_BTN_THRESHOLD_GO  = 22;
constexpr int PIN_LED_PWB_COACH     = 15;  // HIGH = Sufficient ankle offloading on forearms

// I2C Pins for MPU6050 IMU
constexpr int PIN_I2C_SDA           = 8;
constexpr int PIN_I2C_SCL           = 9;
constexpr uint8_t MPU6050_ADDR      = 0x68;

// --- Safety Thresholds ---
constexpr int   FSR_HANDS_PRESENT_THRESHOLD = 600;   // ADC units (0..4095)
constexpr int   FSR_PUSH_ASSIST_THRESHOLD   = 1400;  // Forward push intent
constexpr int   FSR_ANKLE_OFFLOAD_TARGET    = 1800;  // Target forearm load for PWB offloading
constexpr long  MAX_SAFE_HEIGHT_FOR_NARROW  = 350;   // Hall pulses (~500mm seat height)
constexpr long  MAX_PERCH_HEIGHT_PULSES     = 1000;  // ~680mm kitchen counter perch
constexpr int   SYNC_KP                     = 12;    // Proportional gain for L/R sync
constexpr float MAX_SAFE_TILT_DEG           = 12.0f; // Lock wheels & actuators if pitch/roll > 12 deg

enum class SystemState {
  PARKED_LOCKED,
  WALK_ASSIST,
  SIT_TO_STAND_LIFT,
  NARROW_DOOR_MODE,
  EMERGENCY_LOCK
};

volatile long liftPulsesLeft  = 0;
volatile long liftPulsesRight = 0;
SystemState currentState = SystemState::PARKED_LOCKED;
int currentSoftStartPwm = 0;
bool imuAvailable = false;

void IRAM_ATTR onLeftHallPulse()  { liftPulsesLeft++; }
void IRAM_ATTR onRightHallPulse() { liftPulsesRight++; }

void engageHubBrakes(bool lock) {
  digitalWrite(PIN_HUB_BRAKE_EN, lock ? HIGH : LOW);
  if (lock) {
    analogWrite(PIN_HUB_THROTTLE_PWM, 0);
  }
}

void stopVerticalLift() {
  currentSoftStartPwm = 0;
  analogWrite(PIN_LIFT_L_RPWM, 0);
  analogWrite(PIN_LIFT_L_LPWM, 0);
  analogWrite(PIN_LIFT_R_RPWM, 0);
  analogWrite(PIN_LIFT_R_LPWM, 0);
}

bool checkImuTiltFault() {
  if (!imuAvailable) return false;
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x3B); // ACCEL_XOUT_H
  if (Wire.endTransmission(false) != 0) return false;
  Wire.requestFrom(MPU6050_ADDR, (uint8_t)6);
  if (Wire.available() < 6) return false;

  int16_t ax = (Wire.read() << 8) | Wire.read();
  int16_t ay = (Wire.read() << 8) | Wire.read();
  int16_t az = (Wire.read() << 8) | Wire.read();

  float pitch = abs(atan2((float)ax, sqrt((float)ay * ay + (float)az * az)) * 57.2958f);
  float roll  = abs(atan2((float)ay, sqrt((float)ax * ax + (float)az * az)) * 57.2958f);
  return (pitch > MAX_SAFE_TILT_DEG) || (roll > MAX_SAFE_TILT_DEG);
}

// Drives both vertical actuators in closed-loop synchronization with soft-start ramping
void driveSynchronizedLift(bool moveUp, int targetSpeed) {
  currentSoftStartPwm = min(targetSpeed, currentSoftStartPwm + 15);
  long error = liftPulsesLeft - liftPulsesRight;
  int speedL = constrain(currentSoftStartPwm - (error * SYNC_KP), 0, 255);
  int speedR = constrain(currentSoftStartPwm + (error * SYNC_KP), 0, 255);

  if (moveUp) {
    analogWrite(PIN_LIFT_L_RPWM, speedL);
    analogWrite(PIN_LIFT_L_LPWM, 0);
    analogWrite(PIN_LIFT_R_RPWM, speedR);
    analogWrite(PIN_LIFT_R_LPWM, 0);
  } else {
    analogWrite(PIN_LIFT_L_RPWM, 0);
    analogWrite(PIN_LIFT_L_LPWM, speedL);
    analogWrite(PIN_LIFT_R_RPWM, 0);
    analogWrite(PIN_LIFT_R_LPWM, speedR);
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(PIN_HUB_BRAKE_EN, OUTPUT);
  pinMode(PIN_LED_PWB_COACH, OUTPUT);
  engageHubBrakes(true); // Fail-safe: locked on boot

  pinMode(PIN_LIFT_L_HALL, INPUT_PULLUP);
  pinMode(PIN_LIFT_R_HALL, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_LIFT_L_HALL), onLeftHallPulse, RISING);
  attachInterrupt(digitalPinToInterrupt(PIN_LIFT_R_HALL), onRightHallPulse, RISING);

  pinMode(PIN_LIMIT_WIDE, INPUT_PULLUP);
  pinMode(PIN_LIMIT_NARROW, INPUT_PULLUP);
  pinMode(PIN_BTN_LIFT_UP, INPUT_PULLUP);
  pinMode(PIN_BTN_LIFT_DOWN, INPUT_PULLUP);
  pinMode(PIN_BTN_SQUEEZE_MODE, INPUT_PULLUP);
  pinMode(PIN_BTN_THRESHOLD_GO, INPUT_PULLUP);

  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x6B); // PWR_MGMT_1
  Wire.write(0x00); // Wake up MPU6050
  imuAvailable = (Wire.endTransmission() == 0);

  Serial.println("ElderStep Pro Safety Controller Initialized - State: PARKED_LOCKED");
}

void loop() {
  // 0. Highest-Priority IMU Tilt / Stumble Check
  if (checkImuTiltFault()) {
    currentState = SystemState::EMERGENCY_LOCK;
    stopVerticalLift();
    analogWrite(PIN_WIDTH_RPWM, 0);
    analogWrite(PIN_WIDTH_LPWM, 0);
    engageHubBrakes(true);
    Serial.println("EMERGENCY_LOCK: Excessive frame tilt/stumble detected!");
    delay(50);
    return;
  }

  int fsrLeft  = analogRead(PIN_FSR_LEFT);
  int fsrRight = analogRead(PIN_FSR_RIGHT);
  int avgForce = (fsrLeft + fsrRight) / 2;
  bool handsOnForearms = (fsrLeft > FSR_HANDS_PRESENT_THRESHOLD) &&
                         (fsrRight > FSR_HANDS_PRESENT_THRESHOLD);
  bool isWideStance    = (digitalRead(PIN_LIMIT_WIDE) == LOW);
  long avgHeight       = (liftPulsesLeft + liftPulsesRight) / 2;

  // Partial-Weight-Bearing (PWB) Ankle Offloading Coach LED
  digitalWrite(PIN_LED_PWB_COACH, (avgForce >= FSR_ANKLE_OFFLOAD_TARGET) ? HIGH : LOW);

  bool btnUp        = (digitalRead(PIN_BTN_LIFT_UP) == LOW);
  bool btnDown      = (digitalRead(PIN_BTN_LIFT_DOWN) == LOW);
  bool btnSqueeze   = (digitalRead(PIN_BTN_SQUEEZE_MODE) == LOW);
  bool btnThreshold = (digitalRead(PIN_BTN_THRESHOLD_GO) == LOW);

  // 1. Vertical Sit-to-Stand / Kitchen Perch Lift Control (Requires Brakes Locked)
  if (btnUp || btnDown) {
    engageHubBrakes(true);
    // Anti-Tip Interlock: Do not raise above 500mm unless frame is in full Wide Stance (620mm)
    if (btnUp && (!isWideStance && avgHeight >= MAX_SAFE_HEIGHT_FOR_NARROW)) {
      stopVerticalLift();
      Serial.println("INTERLOCK: Widen frame before raising to Kitchen Perch height!");
    } else if (btnUp && avgHeight >= MAX_PERCH_HEIGHT_PULSES) {
      stopVerticalLift();
    } else {
      currentState = SystemState::SIT_TO_STAND_LIFT;
      driveSynchronizedLift(btnUp, 220);
    }
    return;
  } else {
    stopVerticalLift();
  }

  // 2. Width-Morphing Bathroom Squeeze Control (Requires Seat Lowered <= 500mm)
  if (btnSqueeze) {
    engageHubBrakes(true);
    if (avgHeight <= MAX_SAFE_HEIGHT_FOR_NARROW) {
      currentState = SystemState::NARROW_DOOR_MODE;
      analogWrite(PIN_WIDTH_RPWM, 200);
      analogWrite(PIN_WIDTH_LPWM, 0);
    } else {
      Serial.println("INTERLOCK: Lower seat before narrowing frame for bathroom door!");
    }
    return;
  } else {
    analogWrite(PIN_WIDTH_RPWM, 0);
    analogWrite(PIN_WIDTH_LPWM, 0);
  }

  // 3. Dead-Man's Auto-Braking & Touch-Proportional Walking / Threshold Assist
  if (!handsOnForearms) {
    currentState = SystemState::PARKED_LOCKED;
    engageHubBrakes(true);
  } else {
    currentState = SystemState::WALK_ASSIST;
    engageHubBrakes(false);
    if (btnThreshold) {
      // High-torque slow crawl over Indian bathroom doorway marble threshold lip
      analogWrite(PIN_HUB_THROTTLE_PWM, 85);
    } else if (avgForce > FSR_PUSH_ASSIST_THRESHOLD) {
      int assistPwm = map(avgForce, FSR_PUSH_ASSIST_THRESHOLD, 4095, 40, 140);
      // Cap speed to slow crawl if in narrow bathroom doorway stance
      if (!isWideStance) {
        assistPwm = min(assistPwm, 65);
      }
      analogWrite(PIN_HUB_THROTTLE_PWM, assistPwm);
    } else {
      analogWrite(PIN_HUB_THROTTLE_PWM, 0);
    }
  }

  delay(20);
}
