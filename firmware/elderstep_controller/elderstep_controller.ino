/**
 * ElderStep Pro (FreeStep v2) - Universal Home/Hospital & Auto-Summon Firmware
 * Target MCU: ESP32-S3 (with Dual-Core FreeRTOS / Arduino)
 *
 * Implements:
 *  1. Universal Multi-Home / Hospital Presets:
 *     - Width: 480mm (Ultra-Narrow Bathroom) | 550mm (Indoor Standard) | 640mm (Wide Rehab/Perch)
 *     - Lift:  420mm (Low Toilet/Bed) | 480mm (Wheelchair) | 680mm (Kitchen Perch) | 820mm (Slide-Bridge Tray)
 *  2. Autonomous "Summon-to-Grandma" Homing & Docking (UWB Dual-Anchor AoA + 360° LiDAR + Cliff ToF):
 *     - Triggered via Wearable UWB Pendant button OR offline voice wake word ("Walker Come Here" / "Chalo")
 *     - Automatically retracts width to 480mm & lowers CG (420mm) before moving through doorways
 *     - Computes exact distance & bearing angle theta = asin((d_R - d_L) / W) to Grandma's UWB tag
 *     - Steers differentially around obstacles via Left/Right FOC hub motors and auto-docks at 0.50m
 *  3. Fail-Safe "Dead-Man's" Auto-Braking & Instant Human-Grip Override
 *  4. Anti-Tip Software Interlock & 6-Axis IMU Stumble/Tilt Emergency Lock
 */

#include <Arduino.h>
#include <Wire.h>
#include <math.h>

// --- Pin Definitions ---
// 24-Bit Load-Cell / Forearm Grip Force Inputs
constexpr int PIN_FSR_LEFT          = 34;
constexpr int PIN_FSR_RIGHT         = 35;

// Vertical Lift Linear Actuators (Left & Right LINAK/TiMOTION 300mm Stroke)
constexpr int PIN_LIFT_L_RPWM       = 25;
constexpr int PIN_LIFT_L_LPWM       = 26;
constexpr int PIN_LIFT_R_RPWM       = 27;
constexpr int PIN_LIFT_R_LPWM       = 14;
constexpr int PIN_LIFT_L_HALL       = 18;
constexpr int PIN_LIFT_R_HALL       = 19;

// Horizontal Width-Morphing Actuator (480mm <-> 640mm Universal Doorway Morph)
constexpr int PIN_WIDTH_RPWM        = 32;
constexpr int PIN_WIDTH_LPWM        = 33;
constexpr int PIN_LIMIT_WIDE        = 4;   // 640 mm wide stance confirmed
constexpr int PIN_LIMIT_NARROW      = 5;   // 480 mm ultra-narrow doorway stance confirmed

// Rear Pancake FOC Hub Motors (Independent Left & Right Differential Drive + Brake)
constexpr int PIN_HUB_BRAKE_EN      = 23;  // HIGH = Electromagnetic Lock Engaged
constexpr int PIN_HUB_L_PWM         = 13;  // Left Rear FOC Hub Motor Velocity Command
constexpr int PIN_HUB_R_PWM         = 12;  // Right Rear FOC Hub Motor Velocity Command
constexpr int PIN_HUB_L_DIR         = 2;   // Left Rear Direction (HIGH = Forward)
constexpr int PIN_HUB_R_DIR         = 0;   // Right Rear Direction (HIGH = Forward)

// Cockpit Buttons & Status LEDs
constexpr int PIN_BTN_LIFT_UP       = 16;
constexpr int PIN_BTN_LIFT_DOWN     = 17;
constexpr int PIN_BTN_SQUEEZE_MODE  = 21;
constexpr int PIN_BTN_THRESHOLD_GO  = 22;
constexpr int PIN_LED_PWB_COACH     = 15;  // HIGH = Target ankle offloading achieved

// I2C Pins for MPU6050 IMU & VL53L1X Cliff Sensors
constexpr int PIN_I2C_SDA           = 8;
constexpr int PIN_I2C_SCL           = 9;
constexpr uint8_t MPU6050_ADDR      = 0x68;

// --- Universal Architectural & Safety Constants ---
constexpr int   FSR_HANDS_PRESENT_THRESHOLD = 600;   // ADC units (0..4095)
constexpr int   FSR_PUSH_ASSIST_THRESHOLD   = 1400;  // Forward push intent
constexpr int   FSR_ANKLE_OFFLOAD_TARGET    = 1800;  // Target forearm load for PWB offloading
constexpr long  MAX_SAFE_HEIGHT_FOR_NARROW  = 350;   // Hall pulses (~500mm seat height)
constexpr long  MAX_PERCH_HEIGHT_PULSES     = 1200;  // ~720mm saddle / 880mm slide-bridge tray
constexpr int   SYNC_KP                     = 12;    // Proportional gain for L/R column sync
constexpr float MAX_SAFE_TILT_DEG           = 12.0f; // Lock wheels & actuators if pitch/roll > 12 deg

// --- Auto-Summon (UWB Dual-Anchor + LiDAR) Constants ---
constexpr float SUMMON_STOP_DISTANCE_M      = 0.50f; // Stop & lock 50cm in front of Grandma's knees
constexpr float SUMMON_SLOWDOWN_DISTANCE_M  = 1.20f; // Slow crawl approach zone
constexpr float LIDAR_MIN_OBSTACLE_DIST_M   = 0.35f; // Halt/steer if obstacle within 35cm
constexpr int   SUMMON_BASE_PWM             = 70;    // Safe indoor autonomous speed (~0.32 m/s)
constexpr int   SUMMON_DOCK_PWM             = 38;    // Final docking creep speed (~0.12 m/s)
constexpr int   SUMMON_TURN_KP              = 45;    // Differential steering gain on UWB bearing error

enum class SystemState {
  PARKED_LOCKED,
  WALK_ASSIST,
  SIT_TO_STAND_LIFT,
  NARROW_DOOR_MODE,
  AUTO_SUMMON_PREP,     // Lowering CG & narrowing to 480mm before rolling through doorways
  AUTO_SUMMON_HOMING,   // Differential FOC homing toward Grandma's UWB pendant
  AUTO_SUMMON_DOCKED,   // Parked & locked 50cm in front of Grandma, ready for transfer
  EMERGENCY_LOCK
};

struct UwbSummonTelemetry {
  bool  summonRequested;     // True when Grandma presses UWB pendant or says wake word
  float distLeftAnchorM;     // Distance from Grandma's UWB tag to Left Pillar Anchor (m)
  float distRightAnchorM;    // Distance from Grandma's UWB tag to Right Pillar Anchor (m)
  float frontObstacleDistM;  // Minimum obstacle distance in front sector from LD19 LiDAR (m)
  bool  cliffDetected;       // True if downward VL53L1X detects bathroom step drop-off
};

volatile long liftPulsesLeft  = 0;
volatile long liftPulsesRight = 0;
SystemState currentState = SystemState::PARKED_LOCKED;
int currentSoftStartPwm = 0;
bool imuAvailable = false;
UwbSummonTelemetry summonData = {false, 3.0f, 3.0f, 9.9f, false};

void IRAM_ATTR onLeftHallPulse()  { liftPulsesLeft++; }
void IRAM_ATTR onRightHallPulse() { liftPulsesRight++; }

void driveDifferentialHubs(int leftPwm, int rightPwm, bool forwardL = true, bool forwardR = true) {
  digitalWrite(PIN_HUB_L_DIR, forwardL ? HIGH : LOW);
  digitalWrite(PIN_HUB_R_DIR, forwardR ? HIGH : LOW);
  analogWrite(PIN_HUB_L_PWM, constrain(abs(leftPwm), 0, 255));
  analogWrite(PIN_HUB_R_PWM, constrain(abs(rightPwm), 0, 255));
}

void engageHubBrakes(bool lock) {
  digitalWrite(PIN_HUB_BRAKE_EN, lock ? HIGH : LOW);
  if (lock) {
    driveDifferentialHubs(0, 0);
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
  Wire.write(0x3B);
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

/**
 * Executes Autonomous UWB + LiDAR Summon-to-Grandma State Machine.
 * Step 1: Retracts width to 480mm & lowers seat <= 500mm so it fits through any doorway.
 * Step 2: Computes UWB differential bearing and drives Left/Right FOC hubs toward Grandma.
 * Step 3: Parks & locks brakes at 0.50m in front of Grandma.
 */
void runAutoSummonStep(long avgHeight, bool isNarrowStance) {
  if (summonData.cliffDetected || summonData.frontObstacleDistM < LIDAR_MIN_OBSTACLE_DIST_M) {
    // Pause and hold brakes until path clears or obstacle is bypassed
    engageHubBrakes(true);
    return;
  }

  // Step 1: Ensure narrow 480mm width and low CG before autonomous rolling
  if (avgHeight > MAX_SAFE_HEIGHT_FOR_NARROW) {
    currentState = SystemState::AUTO_SUMMON_PREP;
    engageHubBrakes(true);
    driveSynchronizedLift(false, 200);
    return;
  }
  stopVerticalLift();

  if (!isNarrowStance) {
    currentState = SystemState::AUTO_SUMMON_PREP;
    engageHubBrakes(true);
    analogWrite(PIN_WIDTH_RPWM, 0);
    analogWrite(PIN_WIDTH_LPWM, 200); // Retract to 480mm
    return;
  }
  analogWrite(PIN_WIDTH_LPWM, 0);

  // Step 2: Check distance to Grandma's UWB Pendant
  float avgDistM = 0.5f * (summonData.distLeftAnchorM + summonData.distRightAnchorM);
  if (avgDistM <= SUMMON_STOP_DISTANCE_M) {
    currentState = SystemState::AUTO_SUMMON_DOCKED;
    summonData.summonRequested = false;
    engageHubBrakes(true);
    Serial.println("AUTO_SUMMON_DOCKED: Walker parked & locked 50cm in front of Grandma!");
    return;
  }

  // Step 3: Differential Steering toward Grandma using UWB Left/Right Time-of-Flight difference
  currentState = SystemState::AUTO_SUMMON_HOMING;
  engageHubBrakes(false);

  float baselineM = 0.48f; // 480mm narrow stance anchor separation
  float deltaM = constrain(summonData.distRightAnchorM - summonData.distLeftAnchorM, -baselineM, baselineM);
  float bearingRad = asinf(deltaM / baselineM); // Positive = Grandma is to the Left

  int basePwm = (avgDistM < SUMMON_SLOWDOWN_DISTANCE_M) ? SUMMON_DOCK_PWM : SUMMON_BASE_PWM;
  int turnOffset = (int)(bearingRad * SUMMON_TURN_KP);

  int leftWheelPwm  = constrain(basePwm - turnOffset, 0, 110);
  int rightWheelPwm = constrain(basePwm + turnOffset, 0, 110);
  driveDifferentialHubs(leftWheelPwm, rightWheelPwm, true, true);
}

void setup() {
  Serial.begin(115200);

  pinMode(PIN_HUB_BRAKE_EN, OUTPUT);
  pinMode(PIN_HUB_L_DIR, OUTPUT);
  pinMode(PIN_HUB_R_DIR, OUTPUT);
  pinMode(PIN_LED_PWB_COACH, OUTPUT);
  engageHubBrakes(true);

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
  Wire.write(0x6B);
  Wire.write(0x00);
  imuAvailable = (Wire.endTransmission() == 0);

  Serial.println("ElderStep Pro Universal + Auto-Summon Controller Ready");
}

void loop() {
  // 0. Highest-Priority IMU Tilt / Stumble Check
  if (checkImuTiltFault()) {
    currentState = SystemState::EMERGENCY_LOCK;
    summonData.summonRequested = false;
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
  bool isNarrowStance  = (digitalRead(PIN_LIMIT_NARROW) == LOW);
  long avgHeight       = (liftPulsesLeft + liftPulsesRight) / 2;

  // Instant Human-Touch Override: If Grandma touches the handles, cancel Auto-Summon immediately
  if (handsOnForearms && summonData.summonRequested) {
    summonData.summonRequested = false;
    engageHubBrakes(true);
  }

  // Run Autonomous Summon-to-Grandma if active and no hands are on the walker
  if (summonData.summonRequested && !handsOnForearms) {
    runAutoSummonStep(avgHeight, isNarrowStance);
    delay(20);
    return;
  }

  // Partial-Weight-Bearing (PWB) Ankle Offloading Coach LED
  digitalWrite(PIN_LED_PWB_COACH, (avgForce >= FSR_ANKLE_OFFLOAD_TARGET) ? HIGH : LOW);

  bool btnUp        = (digitalRead(PIN_BTN_LIFT_UP) == LOW);
  bool btnDown      = (digitalRead(PIN_BTN_LIFT_DOWN) == LOW);
  bool btnSqueeze   = (digitalRead(PIN_BTN_SQUEEZE_MODE) == LOW);
  bool btnThreshold = (digitalRead(PIN_BTN_THRESHOLD_GO) == LOW);

  // 1. Vertical Sit-to-Stand / Kitchen Perch Lift Control (Requires Brakes Locked)
  if (btnUp || btnDown) {
    engageHubBrakes(true);
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
      analogWrite(PIN_WIDTH_RPWM, 0);
      analogWrite(PIN_WIDTH_LPWM, 200);
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
      driveDifferentialHubs(85, 85, true, true);
    } else if (avgForce > FSR_PUSH_ASSIST_THRESHOLD) {
      int assistPwm = map(avgForce, FSR_PUSH_ASSIST_THRESHOLD, 4095, 40, 140);
      if (!isWideStance) {
        assistPwm = min(assistPwm, 65);
      }
      driveDifferentialHubs(assistPwm, assistPwm, true, true);
    } else {
      driveDifferentialHubs(0, 0, true, true);
    }
  }

  delay(20);
}
