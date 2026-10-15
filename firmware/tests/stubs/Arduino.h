#pragma once
#include <cstdint>
#include <map>
#include <vector>
#include <cmath>
constexpr int HIGH=1, LOW=0, OUTPUT=1, INPUT_PULLDOWN=3;
inline std::map<int,int> pinValues, pinModes;
inline std::vector<std::pair<int,int>> writes;
inline uint32_t clockMs=0;
inline void digitalWrite(int p,int v){pinValues[p]=v;writes.emplace_back(p,v);}
inline void pinMode(int p,int v){pinModes[p]=v;}
inline int digitalRead(int p){return pinValues[p];}
inline int analogRead(int p){return pinValues[p];}
inline void analogReadResolution(int){}
inline uint32_t millis(){return clockMs;}
inline void delay(int ms){clockMs+=ms;}
struct SerialStub{void begin(int){} void println(const char*){}};
inline SerialStub Serial;
