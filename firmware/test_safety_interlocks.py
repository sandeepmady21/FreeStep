#!/usr/bin/env python3
"""
Automated Verification Suite for ElderStep Pro Safety Interlock & Actuator Sync Logic.
Simulates all 6 critical clinical & safety scenarios:
  1. Boot / Hands-Off Fail-Safe Auto-Braking (Dead-Man's Brake)
  2. Kitchen Counter Perch Anti-Tip Interlock (Blocks raising >500mm if narrowed to 490mm)
  3. Bathroom Squeeze Anti-Tip Interlock (Blocks narrowing to 490mm if perched at 680mm)
  4. Closed-Loop Hall Pulse Synchronization (Corrects Left/Right actuator mismatch)
  5. Narrow Doorway Speed Cap (Caps hub assist PWM <= 65 when inside bathroom doorway)
  6. IMU Tilt / Stumble Emergency Lock (>12 deg pitch/roll locks brakes and halts actuators)
"""

import unittest

FSR_HANDS_PRESENT_THRESHOLD = 600
FSR_PUSH_ASSIST_THRESHOLD   = 1400
MAX_SAFE_HEIGHT_FOR_NARROW  = 350
MAX_PERCH_HEIGHT_PULSES     = 1000
SYNC_KP                     = 12
MAX_SAFE_TILT_DEG           = 12.0


def evaluate_controller_step(
    fsr_left=0,
    fsr_right=0,
    is_wide_stance=True,
    pulses_left=0,
    pulses_right=0,
    btn_up=False,
    btn_down=False,
    btn_squeeze=False,
    btn_threshold=False,
    pitch_deg=0.0,
    roll_deg=0.0,
    soft_start_pwm=220,
):
    avg_height = (pulses_left + pulses_right) // 2
    hands_on = (fsr_left > FSR_HANDS_PRESENT_THRESHOLD) and (fsr_right > FSR_HANDS_PRESENT_THRESHOLD)
    avg_force = (fsr_left + fsr_right) // 2

    # 0. IMU Fault Check
    if abs(pitch_deg) > MAX_SAFE_TILT_DEG or abs(roll_deg) > MAX_SAFE_TILT_DEG:
        return {
            "state": "EMERGENCY_LOCK",
            "hub_brake_locked": True,
            "hub_pwm": 0,
            "lift_l_pwm": 0,
            "lift_r_pwm": 0,
            "width_pwm": 0,
        }

    # 1. Vertical Sit-to-Stand / Kitchen Perch Lift
    if btn_up or btn_down:
        if btn_up and (not is_wide_stance and avg_height >= MAX_SAFE_HEIGHT_FOR_NARROW):
            return {
                "state": "INTERLOCK_BLOCKED_LIFT",
                "hub_brake_locked": True,
                "hub_pwm": 0,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
                "width_pwm": 0,
            }
        error = pulses_left - pulses_right
        speed_l = max(0, min(255, soft_start_pwm - error * SYNC_KP))
        speed_r = max(0, min(255, soft_start_pwm + error * SYNC_KP))
        return {
            "state": "SIT_TO_STAND_LIFT",
            "hub_brake_locked": True,
            "hub_pwm": 0,
            "lift_l_pwm": speed_l,
            "lift_r_pwm": speed_r,
            "width_pwm": 0,
        }

    # 2. Width-Morphing Bathroom Squeeze
    if btn_squeeze:
        if avg_height <= MAX_SAFE_HEIGHT_FOR_NARROW:
            return {
                "state": "NARROW_DOOR_MODE",
                "hub_brake_locked": True,
                "hub_pwm": 0,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
                "width_pwm": 200,
            }
        return {
            "state": "INTERLOCK_BLOCKED_SQUEEZE",
            "hub_brake_locked": True,
            "hub_pwm": 0,
            "lift_l_pwm": 0,
            "lift_r_pwm": 0,
            "width_pwm": 0,
        }

    # 3. Dead-Man's Brake & Walking Assist
    if not hands_on:
        return {
            "state": "PARKED_LOCKED",
            "hub_brake_locked": True,
            "hub_pwm": 0,
            "lift_l_pwm": 0,
            "lift_r_pwm": 0,
            "width_pwm": 0,
        }

    hub_pwm = 0
    if btn_threshold:
        hub_pwm = 85
    elif avg_force > FSR_PUSH_ASSIST_THRESHOLD:
        hub_pwm = int(40 + (avg_force - FSR_PUSH_ASSIST_THRESHOLD) * (140 - 40) / (4095 - FSR_PUSH_ASSIST_THRESHOLD))
        if not is_wide_stance:
            hub_pwm = min(hub_pwm, 65)

    return {
        "state": "WALK_ASSIST",
        "hub_brake_locked": False,
        "hub_pwm": hub_pwm,
        "lift_l_pwm": 0,
        "lift_r_pwm": 0,
        "width_pwm": 0,
    }


class TestElderStepSafetyInterlocks(unittest.TestCase):
    def test_dead_mans_auto_brake_when_hands_off(self):
        res = evaluate_controller_step(fsr_left=100, fsr_right=200)
        self.assertEqual(res["state"], "PARKED_LOCKED")
        self.assertTrue(res["hub_brake_locked"])
        self.assertEqual(res["hub_pwm"], 0)

    def test_blocks_kitchen_perch_lift_when_frame_is_narrow(self):
        res = evaluate_controller_step(
            is_wide_stance=False,
            pulses_left=360,
            pulses_right=360,
            btn_up=True,
        )
        self.assertEqual(res["state"], "INTERLOCK_BLOCKED_LIFT")
        self.assertTrue(res["hub_brake_locked"])
        self.assertEqual(res["lift_l_pwm"], 0)
        self.assertEqual(res["lift_r_pwm"], 0)

    def test_blocks_bathroom_squeeze_when_perched_high(self):
        res = evaluate_controller_step(
            is_wide_stance=True,
            pulses_left=800,
            pulses_right=800,
            btn_squeeze=True,
        )
        self.assertEqual(res["state"], "INTERLOCK_BLOCKED_SQUEEZE")
        self.assertEqual(res["width_pwm"], 0)
        self.assertTrue(res["hub_brake_locked"])

    def test_closed_loop_actuator_synchronization(self):
        # Left column is 5 pulses ahead of Right column -> Left slows down, Right speeds up
        res = evaluate_controller_step(
            is_wide_stance=True,
            pulses_left=205,
            pulses_right=200,
            btn_up=True,
            soft_start_pwm=200,
        )
        self.assertEqual(res["state"], "SIT_TO_STAND_LIFT")
        self.assertLess(res["lift_l_pwm"], res["lift_r_pwm"])

    def test_narrow_doorway_speed_cap(self):
        res = evaluate_controller_step(
            fsr_left=3500,
            fsr_right=3500,
            is_wide_stance=False,
        )
        self.assertEqual(res["state"], "WALK_ASSIST")
        self.assertFalse(res["hub_brake_locked"])
        self.assertLessEqual(res["hub_pwm"], 65)

    def test_imu_stumble_emergency_lock(self):
        res = evaluate_controller_step(
            fsr_left=2500,
            fsr_right=2500,
            pitch_deg=15.2,
        )
        self.assertEqual(res["state"], "EMERGENCY_LOCK")
        self.assertTrue(res["hub_brake_locked"])
        self.assertEqual(res["hub_pwm"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
