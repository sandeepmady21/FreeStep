#include "../elderstep_controller/lift_controller.h"
#include <functional>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>
using namespace freestep;
void require(bool v) { if (!v) throw std::runtime_error("assertion failed"); }
void stopped(const Outputs& o) { require(!o.up && !o.down && !o.permit); }
Config commissioned() { Config c; c.commissioned = true; return c; }
struct Fixture {
  LiftController controller;
  Inputs i;
  uint32_t now = 0;
  explicit Fixture(Config c = commissioned()) : controller(c) {
    i.safetyChainHealthy = i.leftBrakeLocked = i.rightBrakeLocked = true;
    i.supportSecured = i.guardClosed = i.oemHealthy = true;
    i.upperClear = i.lowerClear = i.imuHealthy = i.positionHealthy = true;
    i.positionMm = 100;
  }
  Outputs tick(uint32_t delta = 10) {
    now += delta; i.imuSampleMs = now; return controller.step(i, now);
  }
  void arm() {
    for (int n = 0; n < 52; ++n) stopped(tick());
    i.reset = true; require(tick().state == State::Ready);
    i.reset = false; stopped(tick());
  }
  Outputs raise() { i.up = true; auto o = tick(); require(o.up && o.permit && !o.down); return o; }
};
int main() {
  int count = 0;
  auto test = [&](const std::string& name, const std::function<void()>& fn) {
    try { fn(); ++count; std::cout << "PASS " << name << '\n'; }
    catch (...) { std::cerr << "FAIL " << name << '\n'; std::exit(1); }
  };
  test("default configuration cannot move", [] {
    Fixture f{Config{}}; f.i.up = true; auto o = f.tick();
    stopped(o); require(o.fault == Fault::Configuration);
  });
  test("boot and reset do not start a held command", [] {
    Fixture f; f.i.up = f.i.reset = true;
    for (int n=0;n<100;++n) stopped(f.tick());
    f.i.up = false; stopped(f.tick()); // A held reset is not a new edge.
    f.i.reset = false; f.tick(); f.i.reset = true;
    require(f.tick().state == State::Ready);
    f.i.up = true; stopped(f.tick()); // Reset still held.
    f.i.reset = false; stopped(f.tick());
    f.i.up = false; stopped(f.tick()); f.raise();
  });
  test("raise release and lower use the same tested core", [] {
    Fixture f; f.arm(); f.raise(); f.i.up=false; stopped(f.tick());
    f.i.down=true; auto o=f.tick(); require(o.down && o.permit && !o.up);
    f.i.positionMm -= 2; require(f.tick().down);
    f.i.down=false; stopped(f.tick());
  });
  const std::vector<std::pair<std::string, std::function<void(Inputs&)>>> hazards = {
    {"E-stop or broken safety circuit", [](Inputs& i){i.safetyChainHealthy=false;}},
    {"left brake released", [](Inputs& i){i.leftBrakeLocked=false;}},
    {"right brake released", [](Inputs& i){i.rightBrakeLocked=false;}},
    {"support opened", [](Inputs& i){i.supportSecured=false;}},
    {"guard opened", [](Inputs& i){i.guardClosed=false;}},
    {"OEM fault", [](Inputs& i){i.oemHealthy=false;}},
    {"IMU absent", [](Inputs& i){i.imuHealthy=false;}},
    {"excess pitch", [](Inputs& i){i.pitchDeg=4;}},
    {"excess roll", [](Inputs& i){i.rollDeg=-4;}},
    {"NaN tilt", [](Inputs& i){i.rollDeg=std::numeric_limits<float>::quiet_NaN();}},
    {"position disconnected", [](Inputs& i){i.positionHealthy=false;}},
    {"position below calibrated travel", [](Inputs& i){i.positionMm=-1;}},
    {"position above calibrated travel", [](Inputs& i){i.positionMm=251;}},
    {"NaN position", [](Inputs& i){i.positionMm=std::numeric_limits<float>::quiet_NaN();}},
    {"both limits open", [](Inputs& i){i.upperClear=i.lowerClear=false;}},
    {"opposing buttons", [](Inputs& i){i.up=i.down=true;}}
  };
  for (const auto& h : hazards) for (bool lower : {false,true}) {
    test(h.first + (lower ? " stops lowering" : " stops raising"), [&] {
      Fixture f; f.arm(); if(lower){f.i.down=true;require(f.tick().down);}else f.raise();
      h.second(f.i); auto o=f.tick(); stopped(o); require(o.state==State::Fault);
      f.i.up=f.i.down=false; stopped(f.tick());
    });
  }
  test("stale IMU cannot authorize motion", [] {
    Fixture f; f.arm(); f.raise(); f.now+=10; f.i.imuSampleMs=f.now-101;
    auto o=f.controller.step(f.i,f.now); stopped(o); require(o.fault==Fault::Imu);
  });
  test("fault recovery never automatically resumes", [] {
    Fixture f; f.arm(); f.raise(); f.i.guardClosed=false; stopped(f.tick());
    f.i.guardClosed=true;
    for(int n=0;n<60;++n) {auto o=f.tick();stopped(o);require(o.state==State::Fault);}
    f.i.reset=true; stopped(f.tick()); // Up is held: no reset.
    f.i.up=false; f.i.reset=false; f.tick(); f.i.reset=true;
    require(f.tick().state==State::Ready);
    f.i.reset=false; stopped(f.tick()); f.raise();
  });
  test("reset needs a stable healthy interval", [] {
    Fixture f; f.i.reset=true; require(f.tick().state==State::Disarmed);
    f.i.reset=false; f.tick(); f.i.reset=true; require(f.tick().state==State::Disarmed);
  });
  test("hardware and absolute upper limits inhibit only upward movement", [] {
    for(bool physical : {false,true}) {
      Fixture f; f.arm(); f.raise();
      if(physical)f.i.upperClear=false;else f.i.positionMm=250;
      stopped(f.tick()); stopped(f.tick());
      f.i.up=false; f.tick(); f.i.down=true; require(f.tick().down);
    }
  });
  test("hardware and absolute lower limits inhibit only downward movement", [] {
    for(bool physical : {false,true}) {
      Fixture f; f.arm(); f.i.down=true; require(f.tick().down);
      if(physical)f.i.lowerClear=false;else f.i.positionMm=0;
      stopped(f.tick()); f.i.down=false; f.tick(); f.raise();
    }
  });
  test("no direction reversal without neutral", [] {
    Fixture f; f.arm(); f.raise(); f.i.up=false; f.i.down=true;
    stopped(f.tick()); stopped(f.tick());
    f.i.down=false; f.tick(); f.i.down=true; require(f.tick().down);
  });
  test("perch lock stops motion and requires release before restart", [] {
    Fixture f; f.arm(); f.raise(); f.i.perchLockEngaged=true; stopped(f.tick());
    f.i.perchLockEngaged=false; stopped(f.tick());
    f.i.up=false; f.tick(); f.raise();
  });
  test("wrong direction raising and lowering faults", [] {
    for(bool lower : {false,true}) {
      Fixture f; f.arm(); f.i.down=lower; f.i.up=!lower; f.tick();
      f.i.positionMm += lower ? 3 : -3;
      auto o=f.tick();stopped(o);require(o.fault==Fault::WrongDirection);
    }
  });
  test("stalled absolute position faults", [] {
    Fixture f; f.arm(); f.raise(); Outputs o;
    for(int n=0;n<101;++n) o=f.tick();
    stopped(o); require(o.fault==Fault::NoProgress);
  });
  test("continuous movement has a bounded run time", [] {
    auto c=commissioned();c.maxRunMs=100;Fixture f(c);f.arm();f.raise();Outputs o;
    for(int n=0;n<11;++n){f.i.positionMm+=1;o=f.tick();}
    stopped(o);require(o.fault==Fault::RunTimeout);
  });
  test("delayed controller loop latches stop", [] {
    Fixture f;f.arm();f.raise();auto o=f.tick(101);stopped(o);require(o.fault==Fault::LoopTimeout);
  });
  test("uint32 clock rollover preserves timeouts", [] {
    Fixture f;f.now=UINT32_MAX-600;f.arm();f.raise();
    for(int n=0;n<20;++n){f.i.positionMm+=1;require(f.tick().up);}
  });
  test("invalid mechanical settings remain disabled", [] {
    auto c=commissioned();c.maxMm=c.minMm;Fixture f(c);
    auto o=f.tick();stopped(o);require(o.fault==Fault::Configuration);
  });
  std::cout << count << " core regression cases passed\n";
}
