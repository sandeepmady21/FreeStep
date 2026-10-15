#include "../elderstep_controller/elderstep_controller.ino"
#include <iostream>
#include <stdexcept>
void require(bool v){if(!v)throw std::runtime_error("adapter assertion failed");}
void off(){for(int p:pins::outputs)require(pinValues[p]==LOW);}
void healthy(){
 for(int p:{pins::upperClear,pins::lowerClear,pins::safetyHealthy,pins::leftBrake,
     pins::rightBrake,pins::support,pins::guard,pins::oemHealthy})pinValues[p]=HIGH;
 pinValues[pins::position]=1600;
}
void arm(){for(int n=0;n<52;++n)loop();pinValues[pins::resetButton]=HIGH;loop();pinValues[pins::resetButton]=LOW;loop();}
int main(){
 setup();off();healthy();arm();pinValues[pins::upButton]=HIGH;loop();off();
 std::cout<<"PASS shipped Arduino adapter is disabled\n";
 const int idleAlive=pinValues[pins::loopAlive];loop();
 require(pinValues[pins::loopAlive]!=idleAlive);off();
 std::cout<<"PASS independent loop watchdog pulses in disabled idle without motion permission\n";
 // Replace the supervisor ONLY inside this host-side test fixture.
 freestep::Config c;c.commissioned=true;controller=freestep::LiftController(c);
 pinValues[pins::upButton]=LOW;arm();pinValues[pins::upButton]=HIGH;loop();
 require(pinValues[pins::permit]==HIGH && pinValues[pins::upRequest]==HIGH);
 require(pinValues[pins::downRequest]==LOW);
 Wire.healthy=false;loop();off();
 const int faultAlive=pinValues[pins::loopAlive];loop();
 require(pinValues[pins::loopAlive]!=faultAlive);off();
 std::cout<<"PASS actual adapter deasserts all outputs on I2C failure\n";
 Wire.healthy=true;pinValues[pins::upButton]=LOW;arm();
 pinValues[pins::downButton]=HIGH;loop();require(pinValues[pins::downRequest]==HIGH);
 pinValues[pins::guard]=LOW;loop();off();
 std::cout<<"PASS actual adapter stops lowering on guard opening\n";
 for(const auto& w:writes) require(w.first!=22 && w.first!=23 && w.first!=25);
 require(pinModes[pins::position]!=OUTPUT);
 std::cout<<"PASS no writes to missing S3 pins or wheel motor interfaces\n";
}
