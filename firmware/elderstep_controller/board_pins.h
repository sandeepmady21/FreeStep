#pragma once
// ESP32-S3 DevKitC-1. No GPIO22/23/25, flash GPIOs, or USB GPIO19/20.
namespace pins {
constexpr int position = 1; // ADC1
constexpr int upRequest = 4, downRequest = 5, permit = 6;
constexpr int upperClear = 7, lowerClear = 8, safetyHealthy = 9;
constexpr int leftBrake = 10, rightBrake = 11, support = 12, guard = 13;
constexpr int upButton = 14, downButton = 15;
constexpr int sda = 16, scl = 17, resetButton = 18;
constexpr int oemHealthy = 21, heartbeat = 38, perchLock = 39;
constexpr int outputs[] = {upRequest, downRequest, permit, heartbeat};
constexpr int inputs[] = {upperClear, lowerClear, safetyHealthy, leftBrake,
                         rightBrake, support, guard, upButton, downButton,
                         resetButton, oemHealthy, perchLock};
} // namespace pins
