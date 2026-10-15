#pragma once
#include <cstdint>
struct WireStub {
 bool healthy=true; uint8_t reg=0; int idx=0; bool first=true;
 void begin(int,int){} void setTimeOut(int){}
 void beginTransmission(int){first=true;}
 void write(int v){if(first){reg=v;first=false;}}
 int endTransmission(bool=true){return healthy?0:1;}
 int requestFrom(uint8_t,uint8_t count){idx=0;return healthy?count:0;}
 int read(){if(reg==0x75)return 0x68;const int b[]={0,0,0,0,0x40,0};return b[idx++%6];}
};
inline WireStub Wire;
