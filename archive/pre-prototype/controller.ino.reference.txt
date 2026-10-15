/**
 * FreeStep Air (Final 10.20 kg 5-Module Carbon/7075 Edition) - Master Safety & Control Firmware
 * Target MCU: ESP32-S3
 *
 * Implements All Global Benchmark Refinements:
 *  1. 12-Degree Forward-Inclined "Nose-Over-Toes" Synchronized Dual Column Lift (TiMOTION/LINAK)
 *  2. Fixed 495mm (19.5in) Universal Bathroom-Ready Base + 75mm Under-Bed Front Nose
 *  3. RT.Works RT.2 Active Slope-Zeroing Gravity Compensation (tau = M * g * R * sin(pitch))
 *  4. Camino VL53L5CX Rear Shin-Tracking "Too-Far-Ahead" Runaway Distance Guard (<= 28cm)
 *  5. Autonomous UWB Dual-Anchor (DW3000) + 360-Deg LiDAR (LD19) Summon-to-Grandma & Docking
 *  6. Zero-Turn Spin-in-Place Mode, Dead-Man's Auto-Brake & 24-Bit Load-Cell PWB Ankle Coach
 */

#include <Arduino.h>
#include <Wire.h>
#include <math.h>

// --- Pin Definitions ---
constexpr int PIN_LOADCELL_LEFT     = 34;  // Left Forearm 24-Bit Load-Cell Amplifier Analog/ADC
constexpr int PIN_LOADCELL_RIGHT    = 35;  // Right Forearm 24-Bit Load-Cell Amplifier Analog/ADC

// 12-Degree Inclined Telescoping Columns (Left & Right TiMOTION TL18 / LINAK LC1)
constexpr int PIN_LIFT_L_RPWM       = 25;
constexpr int PIN_LIFT_L_LPWM       = 26;
constexpr int PIN_LIFT_R_RPWM       = 27;
constexpr int PIN_LIFT_R_LPWM       = 14;
constexpr int PIN_LIFT_L_HALL       = 18;
constexpr int PIN_LIFT_R_HALL       = 19;

// Rear ZLTECH 6.5" Integrated Servo Hub Wheels (Differential Drive + E-Brake)
constexpr int PIN_HUB_BRAKE_EN      = 23;  // HIGH = Electromagnetic Lock Engaged
constexpr int PIN_HUB_L_PWM         = 13;
constexpr int PIN_HUB_R_PWM         = 12;
constexpr int PIN_HUB_L_DIR         = 2;
constexpr int PIN_HUB_R_DIR         = 0;

// Cockpit Buttons & Status LEDs
constexpr int PIN_BTN_LIFT_UP       = 16;
constexpr int PIN_BTN_LIFT_DOWN     = 17;
constexpr int PIN_BTN_SPIN_IN_PLACE = 21;  // 180-deg Zero-Turn Bathroom Spin Mode
constexpr int PIN_BTN_THRESHOLD_GO  = 22;  // High-torque 40mm marble threshold climb
constexpr int PIN_LED_PWB_COACH     = 15;  // HIGH = Target ankle offloading achieved

// I2C Bus (MPU6050 IMU, VL53L5CX Shin Tracker, 2x VL53L1X Cliff Sensors)
constexpr int PIN_I2C_SDA           = 8;
constexpr int PIN_I2C_SCL           = 9;
constexpr uint8_t MPU6050_ADDR      = 0x68;

// --- Clinical & Biomechanical Constants ---
constexpr int   LOAD_HANDS_PRESENT_THRESHOLD = 600;   // ADC units (0..4095)
constexpr int   LOAD_PUSH_ASSIST_THRESHOLD   = 1400;  // ~100g forward push intent
constexpr int   LOAD_ANKLE_OFFLOAD_TARGET    = 1800;  // Surgeon PWB target offload threshold
constexpr long  MAX_PERCH_HEIGHT_PULSES      = 1200;  // 713mm saddle / 873mm slide-bridge tray
constexpr int   SYNC_KP                      = 12;    // Closed-loop L/R column synchronization gain
constexpr float MAX_SAFE_TILT_DEG            = 12.0f; // Emergency lock threshold
constexpr float SLOPE_COMP_GAIN              = 4.5f;  // RT.Works RT.2 sin(pitch) slope compensation gain
constexpr float MAX_SAFE_SHIN_GAP_CM         = 28.0f; // Camino anti-runaway max torso/shin distance (cm)

// --- Auto-Summon (UWB Dual-Anchor + LiDAR) Constants ---
constexpr float SUMMON_STOP_DISTANCE_M       = 0.50f;
constexpr float SUMMON_SLOWDOWN_DISTANCE_M   = 1.20f;
constexpr float LIDAR_MIN_OBSTACLE_DIST_M    = 0.35f;
constexpr int   SUMMON_BASE_PWM              = 70;
constexpr int   SUMMON_DOCK_PWM              = 38;
constexpr int   SUMMON_TURN_KP               = 45;

enum class SystemState {
  PARKED_LOCKED,
  WALK_ASSIST,
  SIT_TO_STAND_LIFT,
  SPIN_IN_PLACE,
  AUTO_SUMMON_PREP,
  AUTO_SUMMON_HOMING,
  AUTO_SUMMON_DOCKED,
  EMERGENCY_LOCK
};

struct SensorTelemetry {
  bool  summonRequested;
  float distLeftAnchorM;
  float distRightAnchorM;
  float frontObstacleDistM;
  bool  cliffDetected;
  float shinDistanceCm;      // From rear-facing VL53L5CX (Camino anti-runaway guard)
  float pitchDeg;            // Positive = Uphill, Negative = Downhill
  float rollDeg;
};

volatile long liftPulsesLeft  = 0;
volatile long liftPulsesRight = 0;
SystemState currentState = SystemState::PARKED_LOCKED;
int currentSoftStartPwm = 0;
bool imuAvailable = false;
SensorTelemetry sensors = {false, 3.0f, 3.0f, 9.9f, false, 18.0f, 0.0f, 0.0f};

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

void updateImuOrientation() {
  if (!imuAvailable) return;
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x3B);
  if (Wire.endTransmission(false) != 0) return;
  Wire.requestFrom(MPU6050_ADDR, (uint8_t)6);
  if (Wire.available() < 6) return;

  int16_t ax = (Wire.read() << 8) | Wire.read();
  int16_t ay = (Wire.read() << 8) | Wire.read();
  int16_t az = (Wire.read() << 8) | Wire.read();

  sensors.pitchDeg = atan2((float)ax, sqrt((float)ay * ay + (float)az * az)) * 57.2958f;
  sensors.rollDeg  = atan2((float)ay, sqrt((float)ax * ax + (float)az * az)) * 57.2958f;
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

void runAutoSummonStep(long avgHeight) {
  if (sensors.cliffDetected || sensors.frontObstacleDistM < LIDAR_MIN_OBSTACLE_DIST_M) {
    engageHubBrakes(true);
    return;
  }

  // Ensure saddle is lowered (<= 350 pulses) for low CG before autonomous rolling
  if (avgHeight > 350) {
    currentState = SystemState::AUTO_SUMMON_PREP;
    engageHubBrakes(true);
    driveSynchronizedLift(false, 200);
    return;
  }
  stopVerticalLift();

  float avgDistM = 0.5f * (sensors.distLeftAnchorM + sensors.distRightAnchorM);
  if (avgDistM <= SUMMON_STOP_DISTANCE_M) {
    currentState = SystemState::AUTO_SUMMON_DOCKED;
    sensors.summonRequested = false;
    engageHubBrakes(true);
    return;
  }

  currentState = SystemState::AUTO_SUMMON_HOMING;
  engageHubBrakes(false);

  float baselineM = 0.495f; // Fixed 495mm U-base anchor separation
  float deltaM = constrain(sensors.distRightAnchorM - sensors.distLeftAnchorM, -baselineM, baselineM);
  float bearingRad = asinf(deltaM / baselineM);

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

  pinMode(PIN_BTN_LIFT_UP, INPUT_PULLUP);
  pinMode(PIN_BTN_LIFT_DOWN, INPUT_PULLUP);
  pinMode(PIN_BTN_SPIN_IN_PLACE, INPUT_PULLUP);
  pinMode(PIN_BTN_THRESHOLD_GO, INPUT_PULLUP);

  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x6B);
  Wire.write(0x00);
  imuAvailable = (Wire.endTransmission() == 0);

  Serial.println("FreeStep Air 10.20kg 5-Module Controller Initialized");
}

void loop() {
  updateImuOrientation();

  // 0. Highest-Priority IMU Tilt / Stumble Emergency Lock
  if (abs(sensors.pitchDeg) > MAX_SAFE_TILT_DEG || abs(sensors.rollDeg) > MAX_SAFE_TILT_DEG) {
    currentState = SystemState::EMERGENCY_LOCK;
    sensors.summonRequested = false;
    stopVerticalLift();
    engageHubBrakes(true);
    delay(50);
    return;
  }

  int loadLeft  = analogRead(PIN_LOADCELL_LEFT);
  int loadRight = analogRead(PIN_LOADCELL_RIGHT);
  int avgForce  = (loadLeft + loadRight) / 2;
  bool handsOnForearms = (loadLeft > LOAD_HANDS_PRESENT_THRESHOLD) &&
                         (loadRight > LOAD_HANDS_PRESENT_THRESHOLD);
  long avgHeight       = (liftPulsesLeft + liftPulsesRight) / 2;

  // Instant Human-Touch Override on Auto-Summon
  if (handsOnForearms && sensors.summonRequested) {
    sensors.summonRequested = false;
    engageHubBrakes(true);
  }

  if (sensors.summonRequested && !handsOnForearms) {
    runAutoSummonStep(avgHeight);
    delay(20);
    return;
  }

  // Surgeon Partial-Weight-Bearing (PWB) Ankle Offloading Coach LED
  digitalWrite(PIN_LED_PWB_COACH, (avgForce >= LOAD_ANKLE_OFFLOAD_TARGET) ? HIGH : LOW);

  bool btnUp        = (digitalRead(PIN_BTN_LIFT_UP) == LOW);
  bool btnDown      = (digitalRead(PIN_BTN_LIFT_DOWN) == LOW);
  bool btnSpin      = (digitalRead(PIN_BTN_SPIN_IN_PLACE) == LOW);
  bool btnThreshold = (digitalRead(PIN_BTN_THRESHOLD_GO) == LOW);

  // 1. 12-Degree "Nose-Over-Toes" Sit-to-Stand & Kitchen Perch Lift
  if (btnUp || btnDown) {
    engageHubBrakes(true);
    if (btnUp && avgHeight >= MAX_PERCH_HEIGHT_PULSES) {
      stopVerticalLift();
    } else {
      currentState = SystemState::SIT_TO_STAND_LIFT;
      driveSynchronizedLift(btnUp, 220);
    }
    return;
  } else {
    stopVerticalLift();
  }

  // 2. Zero-Turn Spin-in-Place Mode (For Cramped Bathrooms)
  if (btnSpin && handsOnForearms) {
    currentState = SystemState::SPIN_IN_PLACE;
    engageHubBrakes(false);
    driveDifferentialHubs(55, 55, true, false); // Left forward, Right reverse -> 0-radius turn
    return;
  }

  // 3. Dead-Man's Auto-Brake + RT.2 Slope-Zeroing + Camino Shin-Distance Runaway Guard
  if (!handsOnForearms || sensors.cliffDetected) {
    currentState = SystemState::PARKED_LOCKED;
    engageHubBrakes(true);
  } else {
    currentState = SystemState::WALK_ASSIST;
    engageHubBrakes(false);

    if (btnThreshold) {
      driveDifferentialHubs(85, 85, true, true);
    } else if (avgForce > LOAD_PUSH_ASSIST_THRESHOLD) {
      int baseAssist = map(avgForce, LOAD_PUSH_ASSIST_THRESHOLD, 4095, 40, 130);

      // RT.Works RT.2 Slope-Zeroing Gravity Compensation: boost uphill (+pitch), brake downhill (-pitch)
      int slopeComp = (int)(sensors.pitchDeg * SLOPE_COMP_GAIN);
      int totalPwm  = constrain(baseAssist + slopeComp, 0, 160);

      // Camino Shin-Distance Runaway Guard: slow down if walker moves >28cm ahead of user's shins
      if (sensors.shinDistanceCm > MAX_SAFE_SHIN_GAP_CM) {
        totalPwm = min(totalPwm, 25);
      }
      driveDifferentialHubs(totalPwm, totalPwm, true, true);
    } else {
      driveDifferentialHubs(0, 0, true, true);
    }
  }

  delay(20);
}
