#pragma once

#include <cmath>
#include <cstdint>

// Bench supervisor shared by the Arduino adapter and native regression tests.
// This is not a safety-rated motion controller. Independent hardware must remove
// the OEM lift's run permission on an E-stop, open guard, or lost heartbeat.
namespace freestep {
enum class State { Disarmed, Ready, Raising, Lowering, Fault };
enum class Fault {
  None, Configuration, SafetyChain, Brake, Support, Guard, Oem,
  Imu, Tilt, Position, Limits, Buttons, LoopTimeout, RunTimeout,
  NoProgress, WrongDirection
};
struct Config {
  bool commissioned = false;  // Remains false in the supplied bench build.
  float minMm = 0;
  float maxMm = 250;
  float maxTiltDeg = 3;
  float progressMm = 1;
  float reverseToleranceMm = 2;
  uint32_t stableMs = 500;
  uint32_t imuMaxAgeMs = 100;
  uint32_t loopMaxGapMs = 100;
  uint32_t stallMs = 1000;
  uint32_t maxRunMs = 10000;
};
struct Inputs {
  bool safetyChainHealthy = false;
  bool leftBrakeLocked = false;
  bool rightBrakeLocked = false;
  bool supportSecured = false;
  bool guardClosed = false;
  bool oemHealthy = false;
  bool upperClear = false; // NC direction limit: open inhibits raising.
  bool lowerClear = false; // NC direction limit: open inhibits lowering.
  bool perchLockEngaged = false; // Positive mechanical rest lock; no motion.
  bool imuHealthy = false;
  uint32_t imuSampleMs = 0;
  float pitchDeg = 0;
  float rollDeg = 0;
  bool positionHealthy = false;
  float positionMm = 0; // Absolute transducer, not a volatile pulse counter.
  bool up = false;
  bool down = false;
  bool reset = false;
};
struct Outputs {
  State state = State::Disarmed;
  Fault fault = Fault::None;
  bool up = false;
  bool down = false;
  bool permit = false;
};

class LiftController {
 public:
  explicit LiftController(Config config = {}) : config_(config) {}
  Outputs step(const Inputs& i, uint32_t now) {
    const bool resetEdge = i.reset && !previousReset_;
    previousReset_ = i.reset;
    const bool wasMoving = moving();
    const bool loopLate = tickSeen_ && uint32_t(now - lastTick_) > config_.loopMaxGapMs;
    tickSeen_ = true;
    lastTick_ = now;
    Fault hazard = check(i, now);
    if (hazard == Fault::None && loopLate && wasMoving) hazard = Fault::LoopTimeout;
    if (hazard != Fault::None) {
      stableTracking_ = false;
      return fail(hazard);
    }
    if (!stableTracking_) { safeSince_ = now; stableTracking_ = true; }

    if (state_ == State::Disarmed || state_ == State::Fault) {
      // Reset must be a new edge after recovery, with the pendant released.
      if (resetEdge && !i.up && !i.down &&
          uint32_t(now - safeSince_) >= config_.stableMs) {
        state_ = State::Ready;
        fault_ = Fault::None;
        neutralRequired_ = true;
      }
      return stopped();
    }
    if (i.reset || i.perchLockEngaged || (!i.up && !i.down)) {
      state_ = State::Ready;
      neutralRequired_ = i.reset || i.perchLockEngaged;
      return stopped();
    }
    if (neutralRequired_) return stopped();
    const State requested = i.up ? State::Raising : State::Lowering;
    // A reversal always requires a neutral pendant sample first.
    if (wasMoving && requested != state_) {
      state_ = State::Ready;
      neutralRequired_ = true;
      return stopped();
    }
    if ((i.up && (!i.upperClear || i.positionMm >= config_.maxMm)) ||
        (i.down && (!i.lowerClear || i.positionMm <= config_.minMm))) {
      state_ = State::Ready;
      neutralRequired_ = true;
      return stopped();
    }
    if (!wasMoving) {
      runSince_ = progressSince_ = now;
      progressPosition_ = i.positionMm;
    }
    state_ = requested;
    const float advance = (i.positionMm - progressPosition_) * (i.up ? 1 : -1);
    if (advance < -config_.reverseToleranceMm) return fail(Fault::WrongDirection);
    if (advance >= config_.progressMm) {
      progressPosition_ = i.positionMm;
      progressSince_ = now;
    }
    if (uint32_t(now - runSince_) >= config_.maxRunMs) return fail(Fault::RunTimeout);
    if (uint32_t(now - progressSince_) >= config_.stallMs) return fail(Fault::NoProgress);
    return {state_, fault_, i.up, i.down, true};
  }

 private:
  bool moving() const { return state_ == State::Raising || state_ == State::Lowering; }
  Outputs stopped() const { return {state_, fault_, false, false, false}; }
  Outputs fail(Fault f) {
    // Keep the first fault until a deliberate reset; all paths remove requests.
    if (state_ != State::Fault) fault_ = f;
    state_ = State::Fault;
    neutralRequired_ = true;
    return stopped();
  }
  Fault check(const Inputs& i, uint32_t now) const {
    if (!config_.commissioned || !std::isfinite(config_.minMm) ||
        !std::isfinite(config_.maxMm) || config_.maxMm <= config_.minMm ||
        !std::isfinite(config_.maxTiltDeg) || config_.maxTiltDeg <= 0 ||
        !std::isfinite(config_.progressMm) || config_.progressMm <= 0 ||
        !std::isfinite(config_.reverseToleranceMm) || config_.reverseToleranceMm < 0 ||
        config_.stableMs == 0 || config_.imuMaxAgeMs == 0 ||
        config_.loopMaxGapMs == 0 || config_.stallMs == 0 || config_.maxRunMs == 0)
      return Fault::Configuration;
    if (!i.safetyChainHealthy) return Fault::SafetyChain;
    if (!i.leftBrakeLocked || !i.rightBrakeLocked) return Fault::Brake;
    if (!i.supportSecured) return Fault::Support;
    if (!i.guardClosed) return Fault::Guard;
    if (!i.oemHealthy) return Fault::Oem;
    if (!i.imuHealthy || uint32_t(now - i.imuSampleMs) > config_.imuMaxAgeMs ||
        !std::isfinite(i.pitchDeg) || !std::isfinite(i.rollDeg)) return Fault::Imu;
    if (std::fabs(i.pitchDeg) > config_.maxTiltDeg ||
        std::fabs(i.rollDeg) > config_.maxTiltDeg) return Fault::Tilt;
    if (!i.positionHealthy || !std::isfinite(i.positionMm) ||
        i.positionMm < config_.minMm || i.positionMm > config_.maxMm) return Fault::Position;
    if (!i.upperClear && !i.lowerClear) return Fault::Limits;
    if (i.up && i.down) return Fault::Buttons;
    return Fault::None;
  }
  Config config_;
  State state_ = State::Disarmed;
  Fault fault_ = Fault::None;
  bool previousReset_ = false, tickSeen_ = false;
  bool neutralRequired_ = true, stableTracking_ = false;
  uint32_t lastTick_ = 0, safeSince_ = 0, runSince_ = 0, progressSince_ = 0;
  float progressPosition_ = 0;
};
} // namespace freestep
