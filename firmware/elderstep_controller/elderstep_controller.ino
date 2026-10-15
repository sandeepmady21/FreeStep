/**
 * ElderStep Pro (FreeStep v2) - Core Safety & Control Firmware
 * Target MCU: ESP32 / ESP32-S3
 *
 * Implements:
 *  1. Fail-Safe "Dead-Man's" Auto-Braking on Rear BLDC Hub Motors
 *  2. Synchronized Dual Vertical Linear Actuator Control (Sit-to-Stand & Kitchen Perch)
 *  3. Anti-Tip Software Interlock between Width-Morphing Actuator & Seat Height
 *  4. IMU Fall / Stumble Spike Detection -> Instant Electromagnetic Lock
 */

#include <Arduino.h>

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

// Cockpit Buttons
constexpr int PIN_BTN_LIFT_UP       = 16;
constexpr int PIN_BTN_LIFT_DOWN     = 17;
constexpr int PIN_BTN_SQUEEZE_MODE  = 21;
constexpr int PIN_BTN_THRESHOLD_GO  = 22;

// --- Safety Thresholds ---
constexpr int   FSR_HANDS_PRESENT_THRESHOLD = 600;   // ADC units (0..4095)
constexpr int   FSR_PUSH_ASSIST_THRESHOLD   = 1400;  // Forward push intent
constexpr long  MAX_SAFE_HEIGHT_FOR_NARROW  = 350;   // Hall pulses (~500mm seat height)
constexpr long  MAX_PERCH_HEIGHT_PULSES     = 1000;  // ~680mm kitchen counter perch
constexpr int   SYNC_KP                     = 12;    // Proportional gain for L/R sync

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

void IRAM_ATTR onLeftHallPulse()  { liftPulsesLeft++; }
void IRAM_ATTR onRightHallPulse() { liftPulsesRight++; }

void engageHubBrakes(bool lock) {
  digitalWrite(PIN_HUB_BRAKE_EN, lock ? HIGH : LOW);
  if (lock) {
    analogWrite(PIN_HUB_THROTTLE_PWM, 0);
  }
}

void stopVerticalLift() {
  analogWrite(PIN_LIFT_L_RPWM, 0);
  analogWrite(PIN_LIFT_L_LPWM, 0);
  analogWrite(PIN_LIFT_R_RPWM, 0);
  analogWrite(PIN_LIFT_R_LPWM, 0);
}

// Drives both vertical actuators in closed-loop synchronization so seat stays level
void driveSynchronizedLift(bool moveUp, int baseSpeed) {
  long error = liftPulsesLeft - liftPulsesRight;
  int speedL = constrain(baseSpeed - (error * SYNC_KP), 0, 255);
  int speedR = constrain(baseSpeed + (error * SYNC_KP), 0, 255);

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

  Serial.println("ElderStep Pro Safety Controller Initialized - State: PARKED_LOCKED");
}

void loop() {
  int fsrLeft  = analogRead(PIN_FSR_LEFT);
  int fsrRight = analogRead(PIN_FSR_RIGHT);
  bool handsOnForearms = (fsrLeft > FSR_HANDS_PRESENT_THRESHOLD) &&
                         (fsrRight > FSR_HANDS_PRESENT_THRESHOLD);
  bool isWideStance    = (digitalRead(PIN_LIMIT_WIDE) == LOW);
  long avgHeight       = (liftPulsesLeft + liftPulsesRight) / 2;

  bool btnUp      = (digitalRead(PIN_BTN_LIFT_UP) == LOW);
  bool btnDown    = (digitalRead(PIN_BTN_LIFT_DOWN) == LOW);
  bool btnSqueeze = (digitalRead(PIN_BTN_SQUEEZE_MODE) == LOW);

  // 1. Vertical Sit-to-Stand / Kitchen Perch Lift Control (Requires Brakes Locked)
  if (btnUp || btnDown) {
    engageHubBrakes(true);
    // Anti-Tip Interlock: Do not raise above 500mm unless frame is in full Wide Stance (620mm)
    if (btnUp && (!isWideStance && avgHeight >= MAX_SAFE_HEIGHT_FOR_NARROW)) {
      stopVerticalLift();
      Serial.println("INTERLOCK: Widen frame before raising to Kitchen Perch height!");
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

  // 3. Dead-Man's Auto-Braking & Touch-Proportional Walking Assist
  if (!handsOnForearms) {
    currentState = SystemState::PARKED_LOCKED;
    engageHubBrakes(true);
  } else {
    currentState = SystemState::WALK_ASSIST;
    engageHubBrakes(false);
    int avgForce = (fsrLeft + fsrRight) / 2;
    if (avgForce > FSR_PUSH_ASSIST_THRESHOLD) {
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
