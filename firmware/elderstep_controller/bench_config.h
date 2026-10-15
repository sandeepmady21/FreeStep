#pragma once

// Deliberately disabled. These are fixture placeholders, not patient settings.
// Complete hardware/VALIDATION_PLAN.md and review the actual OEM lift interface
// before enabling an UNLOADED BENCH fixture. This flag never authorizes human use.
constexpr bool BENCH_COMMISSIONED = false;
constexpr int POSITION_ADC_LOW = 400;
constexpr int POSITION_ADC_HIGH = 3600;
constexpr float LIFT_TRAVEL_MM = 250.0f;
