/** FreeStep P0: single-lift bench supervisor. NO wheel motor outputs.
 * Uncommissioned by default; not for human use. See hardware/ before wiring.
 * Outputs request motion from a separately protected OEM controller through
 * isolated interfaces. Never connect a motor, relay coil or 24V contact to GPIO.
 */
#include <Arduino.h>
#include <Wire.h>
#include "bench_config.h"
#include "board_pins.h"
#include "lift_controller.h"

freestep::Config makeConfig() {
  freestep::Config c;
  c.commissioned = BENCH_COMMISSIONED && POSITION_ADC_LOW > 100 &&
      POSITION_ADC_HIGH < 3995 && POSITION_ADC_HIGH > POSITION_ADC_LOW;
  c.maxMm = LIFT_TRAVEL_MM;
  return c;
}
freestep::LiftController controller(makeConfig());
bool heartbeatLevel = false;
bool imuInitialized = false;
constexpr uint8_t IMU_ADDRESS = 0x68;

bool readRegisters(uint8_t reg, uint8_t* bytes, uint8_t count) {
  Wire.beginTransmission(IMU_ADDRESS);
  Wire.write(reg);
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom(IMU_ADDRESS, count) != count) return false;
  for (uint8_t n = 0; n < count; ++n) bytes[n] = Wire.read();
  return true;
}

bool readImu(freestep::Inputs& i) {
  if (!imuInitialized) return false;
  uint8_t b[6];
  if (!readRegisters(0x3B, b, 6)) return false;
  const float ax = int16_t((uint16_t(b[0]) << 8) | b[1]) / 16384.0f;
  const float ay = int16_t((uint16_t(b[2]) << 8) | b[3]) / 16384.0f;
  const float az = int16_t((uint16_t(b[4]) << 8) | b[5]) / 16384.0f;
  const float norm = sqrtf(ax * ax + ay * ay + az * az);
  // Quasi-static fixture only. Reject implausible data and substantial motion.
  if (norm < 0.8f || norm > 1.2f || az < 0.5f) return false;
  i.pitchDeg = atan2f(ax, sqrtf(ay * ay + az * az)) * 57.29578f;
  i.rollDeg = atan2f(ay, sqrtf(ax * ax + az * az)) * 57.29578f;
  i.imuSampleMs = millis();
  return true;
}

void applyOutputs(const freestep::Outputs& o) {
  static int direction = 0;
  const int next = o.permit ? (o.up ? 1 : (o.down ? -1 : 0)) : 0;
  if (next != direction || next == 0) {
    digitalWrite(pins::permit, LOW);
    digitalWrite(pins::upRequest, LOW);
    digitalWrite(pins::downRequest, LOW);
  }
  direction = next;
  if (next != 0) {
    digitalWrite(pins::upRequest, next > 0 ? HIGH : LOW);
    digitalWrite(pins::downRequest, next < 0 ? HIGH : LOW);
    digitalWrite(pins::permit, HIGH);
    heartbeatLevel = !heartbeatLevel;
  } else heartbeatLevel = false;
  digitalWrite(pins::heartbeat, heartbeatLevel ? HIGH : LOW);
}

void setup() {
  for (int p : pins::outputs) { digitalWrite(p, LOW); pinMode(p, OUTPUT); }
  // External 10k pulldowns are also required; open contacts are unhealthy.
  for (int p : pins::inputs) pinMode(p, INPUT_PULLDOWN);
  analogReadResolution(12);
  Wire.begin(pins::sda, pins::scl);
  Wire.setTimeOut(10);
  uint8_t identity = 0;
  if (readRegisters(0x75, &identity, 1) && identity == 0x68) {
    Wire.beginTransmission(IMU_ADDRESS);
    Wire.write(0x6B); Wire.write(0);
    imuInitialized = Wire.endTransmission() == 0;
    // Explicit +/-2g range for the scale used in readImu().
    Wire.beginTransmission(IMU_ADDRESS);
    Wire.write(0x1C); Wire.write(0);
    imuInitialized = (Wire.endTransmission() == 0) && imuInitialized;
  }
  Serial.begin(115200);
  Serial.println("FreeStep P0 BENCH ONLY; commissioned=false in supplied build");
}

void loop() {
  freestep::Inputs i;
  i.safetyChainHealthy = digitalRead(pins::safetyHealthy) == HIGH;
  i.leftBrakeLocked = digitalRead(pins::leftBrake) == HIGH;
  i.rightBrakeLocked = digitalRead(pins::rightBrake) == HIGH;
  i.supportSecured = digitalRead(pins::support) == HIGH;
  i.guardClosed = digitalRead(pins::guard) == HIGH;
  i.oemHealthy = digitalRead(pins::oemHealthy) == HIGH;
  i.upperClear = digitalRead(pins::upperClear) == HIGH;
  i.lowerClear = digitalRead(pins::lowerClear) == HIGH;
  i.perchLockEngaged = digitalRead(pins::perchLock) == HIGH;
  i.up = digitalRead(pins::upButton) == HIGH;
  i.down = digitalRead(pins::downButton) == HIGH;
  i.reset = digitalRead(pins::resetButton) == HIGH;
  const int raw = analogRead(pins::position);
  i.positionHealthy = raw >= POSITION_ADC_LOW && raw <= POSITION_ADC_HIGH;
  i.positionMm = float(raw - POSITION_ADC_LOW) * LIFT_TRAVEL_MM /
      float(POSITION_ADC_HIGH - POSITION_ADC_LOW);
  i.imuHealthy = readImu(i);
  const auto o = controller.step(i, millis());
  applyOutputs(o);
  // No blocking logging in the motion path. External hardware heartbeat timeout
  // must remove permission independently of this CPU and its I2C/loop timing.
  delay(10);
}
