#!/usr/bin/env python3
"""
Automated Verification Suite for ElderStep Pro Universal & Auto-Summon Controller.
Verifies 11 critical clinical, universal doorway/counter, and autonomous summon scenarios:
  1. Boot / Hands-Off Fail-Safe Auto-Braking (Dead-Man's Brake)
  2. Kitchen Counter Perch Anti-Tip Interlock (Blocks raising >500mm if narrowed to 480mm)
  3. Bathroom Squeeze Anti-Tip Interlock (Blocks narrowing to 480mm if perched high)
  4. Closed-Loop Hall Pulse Synchronization (Corrects Left/Right actuator mismatch)
  5. Narrow Doorway Speed Cap (Caps hub assist PWM <= 65 when inside bathroom doorway)
  6. IMU Tilt / Stumble Emergency Lock (>12 deg pitch/roll locks brakes and halts actuators)
  7. Auto-Summon Prep: Automatically lowers high seat & retracts width to 480mm before rolling
  8. Auto-Summon UWB Homing: Steers Left/Right FOC hubs toward Grandma's UWB Pendant bearing
  9. Auto-Summon Obstacle & Cliff Protection: Halts and locks brakes if LiDAR/ToF sees obstacle <35cm
 10. Auto-Summon Docking: Stops and engages electromagnetic parking brake at 50cm from Grandma
 11. Instant Human-Grip Override: Cancels autonomous summon the instant forearms touch the pads
"""

import math
import unittest

FSR_HANDS_PRESENT_THRESHOLD = 600
FSR_PUSH_ASSIST_THRESHOLD   = 1400
MAX_SAFE_HEIGHT_FOR_NARROW  = 350
MAX_PERCH_HEIGHT_PULSES     = 1200
SYNC_KP                     = 12
MAX_SAFE_TILT_DEG           = 12.0

SUMMON_STOP_DISTANCE_M      = 0.50
SUMMON_SLOWDOWN_DISTANCE_M  = 1.20
LIDAR_MIN_OBSTACLE_DIST_M   = 0.35
SUMMON_BASE_PWM             = 70
SUMMON_DOCK_PWM             = 38
SUMMON_TURN_KP              = 45


def evaluate_controller_step(
    fsr_left=0,
    fsr_right=0,
    is_wide_stance=True,
    is_narrow_stance=False,
    pulses_left=0,
    pulses_right=0,
    btn_up=False,
    btn_down=False,
    btn_squeeze=False,
    btn_threshold=False,
    pitch_deg=0.0,
    roll_deg=0.0,
    soft_start_pwm=220,
    summon_requested=False,
    uwb_dist_left_m=3.0,
    uwb_dist_right_m=3.0,
    lidar_front_obstacle_m=9.9,
    cliff_detected=False,
):
    avg_height = (pulses_left + pulses_right) // 2
    hands_on = (fsr_left > FSR_HANDS_PRESENT_THRESHOLD) and (fsr_right > FSR_HANDS_PRESENT_THRESHOLD)
    avg_force = (fsr_left + fsr_right) // 2

    # 0. IMU Fault Check
    if abs(pitch_deg) > MAX_SAFE_TILT_DEG or abs(roll_deg) > MAX_SAFE_TILT_DEG:
        return {
            "state": "EMERGENCY_LOCK",
            "summon_active": False,
            "hub_brake_locked": True,
            "hub_l_pwm": 0,
            "hub_r_pwm": 0,
            "lift_l_pwm": 0,
            "lift_r_pwm": 0,
            "width_pwm": 0,
        }

    # Instant Human-Grip Override on Auto-Summon
    if hands_on and summon_requested:
        summon_requested = False

    # Autonomous Summon-to-Grandma Mode
    if summon_requested and not hands_on:
        if cliff_detected or lidar_front_obstacle_m < LIDAR_MIN_OBSTACLE_DIST_M:
            return {
                "state": "AUTO_SUMMON_OBSTACLE_HOLD",
                "summon_active": True,
                "hub_brake_locked": True,
                "hub_l_pwm": 0,
                "hub_r_pwm": 0,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
                "width_pwm": 0,
            }
        if avg_height > MAX_SAFE_HEIGHT_FOR_NARROW:
            return {
                "state": "AUTO_SUMMON_PREP",
                "summon_active": True,
                "hub_brake_locked": True,
                "hub_l_pwm": 0,
                "hub_r_pwm": 0,
                "lift_l_pwm": 200,
                "lift_r_pwm": 200,
                "width_pwm": 0,
            }
        if not is_narrow_stance:
            return {
                "state": "AUTO_SUMMON_PREP",
                "summon_active": True,
                "hub_brake_locked": True,
                "hub_l_pwm": 0,
                "hub_r_pwm": 0,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
                "width_pwm": 200,
            }
        avg_dist = 0.5 * (uwb_dist_left_m + uwb_dist_right_m)
        if avg_dist <= SUMMON_STOP_DISTANCE_M:
            return {
                "state": "AUTO_SUMMON_DOCKED",
                "summon_active": False,
                "hub_brake_locked": True,
                "hub_l_pwm": 0,
                "hub_r_pwm": 0,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
                "width_pwm": 0,
            }
        baseline = 0.48
        delta = max(-baseline, min(baseline, uwb_dist_right_m - uwb_dist_left_m))
        bearing_rad = math.asin(delta / baseline)
        base_pwm = SUMMON_DOCK_PWM if avg_dist < SUMMON_SLOWDOWN_DISTANCE_M else SUMMON_BASE_PWM
        turn_offset = int(bearing_rad * SUMMON_TURN_KP)
        l_pwm = max(0, min(110, base_pwm - turn_offset))
        r_pwm = max(0, min(110, base_pwm + turn_offset))
        return {
            "state": "AUTO_SUMMON_HOMING",
            "summon_active": True,
            "hub_brake_locked": False,
            "hub_l_pwm": l_pwm,
            "hub_r_pwm": r_pwm,
            "lift_l_pwm": 0,
            "lift_r_pwm": 0,
            "width_pwm": 0,
        }

    # 1. Vertical Sit-to-Stand / Kitchen Perch Lift
    if btn_up or btn_down:
        if btn_up and (not is_wide_stance and avg_height >= MAX_SAFE_HEIGHT_FOR_NARROW):
            return {
                "state": "INTERLOCK_BLOCKED_LIFT",
                "summon_active": False,
                "hub_brake_locked": True,
                "hub_l_pwm": 0,
                "hub_r_pwm": 0,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
                "width_pwm": 0,
            }
        error = pulses_left - pulses_right
        speed_l = max(0, min(255, soft_start_pwm - error * SYNC_KP))
        speed_r = max(0, min(255, soft_start_pwm + error * SYNC_KP))
        return {
            "state": "SIT_TO_STAND_LIFT",
            "summon_active": False,
            "hub_brake_locked": True,
            "hub_l_pwm": 0,
            "hub_r_pwm": 0,
            "lift_l_pwm": speed_l,
            "lift_r_pwm": speed_r,
            "width_pwm": 0,
        }

    # 2. Width-Morphing Bathroom Squeeze
    if btn_squeeze:
        if avg_height <= MAX_SAFE_HEIGHT_FOR_NARROW:
            return {
                "state": "NARROW_DOOR_MODE",
                "summon_active": False,
                "hub_brake_locked": True,
                "hub_l_pwm": 0,
                "hub_r_pwm": 0,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
                "width_pwm": 200,
            }
        return {
            "state": "INTERLOCK_BLOCKED_SQUEEZE",
            "summon_active": False,
            "hub_brake_locked": True,
            "hub_l_pwm": 0,
            "hub_r_pwm": 0,
            "lift_l_pwm": 0,
            "lift_r_pwm": 0,
            "width_pwm": 0,
        }

    # 3. Dead-Man's Brake & Walking Assist
    if not hands_on:
        return {
            "state": "PARKED_LOCKED",
            "summon_active": False,
            "hub_brake_locked": True,
            "hub_l_pwm": 0,
            "hub_r_pwm": 0,
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
        "summon_active": False,
        "hub_brake_locked": False,
        "hub_l_pwm": hub_pwm,
        "hub_r_pwm": hub_pwm,
        "lift_l_pwm": 0,
        "lift_r_pwm": 0,
        "width_pwm": 0,
    }


class TestElderStepUniversalAndAutoSummon(unittest.TestCase):
    def test_01_dead_mans_auto_brake_when_hands_off(self):
        res = evaluate_controller_step(fsr_left=100, fsr_right=200)
        self.assertEqual(res["state"], "PARKED_LOCKED")
        self.assertTrue(res["hub_brake_locked"])

    def test_02_blocks_kitchen_perch_lift_when_frame_is_narrow(self):
        res = evaluate_controller_step(is_wide_stance=False, pulses_left=360, pulses_right=360, btn_up=True)
        self.assertEqual(res["state"], "INTERLOCK_BLOCKED_LIFT")
        self.assertTrue(res["hub_brake_locked"])

    def test_03_blocks_bathroom_squeeze_when_perched_high(self):
        res = evaluate_controller_step(is_wide_stance=True, pulses_left=800, pulses_right=800, btn_squeeze=True)
        self.assertEqual(res["state"], "INTERLOCK_BLOCKED_SQUEEZE")
        self.assertEqual(res["width_pwm"], 0)

    def test_04_closed_loop_actuator_synchronization(self):
        res = evaluate_controller_step(is_wide_stance=True, pulses_left=205, pulses_right=200, btn_up=True, soft_start_pwm=200)
        self.assertEqual(res["state"], "SIT_TO_STAND_LIFT")
        self.assertLess(res["lift_l_pwm"], res["lift_r_pwm"])

    def test_05_narrow_doorway_speed_cap(self):
        res = evaluate_controller_step(fsr_left=3500, fsr_right=3500, is_wide_stance=False)
        self.assertEqual(res["state"], "WALK_ASSIST")
        self.assertLessEqual(res["hub_l_pwm"], 65)

    def test_06_imu_stumble_emergency_lock(self):
        res = evaluate_controller_step(fsr_left=2500, fsr_right=2500, pitch_deg=15.2)
        self.assertEqual(res["state"], "EMERGENCY_LOCK")
        self.assertTrue(res["hub_brake_locked"])

    def test_07_auto_summon_prep_lowers_and_narrows_for_doorways(self):
        # If walker is wide when summoned, it narrows to 480mm first before moving
        res = evaluate_controller_step(summon_requested=True, is_narrow_stance=False, pulses_left=200, pulses_right=200)
        self.assertEqual(res["state"], "AUTO_SUMMON_PREP")
        self.assertTrue(res["hub_brake_locked"])
        self.assertEqual(res["width_pwm"], 200)

    def test_08_auto_summon_uwb_differential_steering_to_grandma(self):
        # Grandma is to the LEFT (distLeft < distRight) -> Right wheel drives faster than Left wheel to turn Left
        res = evaluate_controller_step(
            summon_requested=True,
            is_narrow_stance=True,
            pulses_left=100,
            pulses_right=100,
            uwb_dist_left_m=2.00,
            uwb_dist_right_m=2.25,
        )
        self.assertEqual(res["state"], "AUTO_SUMMON_HOMING")
        self.assertFalse(res["hub_brake_locked"])
        self.assertGreater(res["hub_r_pwm"], res["hub_l_pwm"])

    def test_09_auto_summon_lidar_obstacle_and_cliff_protection(self):
        res = evaluate_controller_step(
            summon_requested=True,
            is_narrow_stance=True,
            lidar_front_obstacle_m=0.22,
        )
        self.assertEqual(res["state"], "AUTO_SUMMON_OBSTACLE_HOLD")
        self.assertTrue(res["hub_brake_locked"])

    def test_10_auto_summon_docks_and_locks_at_50cm(self):
        res = evaluate_controller_step(
            summon_requested=True,
            is_narrow_stance=True,
            uwb_dist_left_m=0.48,
            uwb_dist_right_m=0.49,
        )
        self.assertEqual(res["state"], "AUTO_SUMMON_DOCKED")
        self.assertFalse(res["summon_active"])
        self.assertTrue(res["hub_brake_locked"])

    def test_11_human_grip_instantly_overrides_auto_summon(self):
        res = evaluate_controller_step(
            fsr_left=1000,
            fsr_right=1000,
            summon_requested=True,
            is_narrow_stance=True,
            uwb_dist_left_m=2.0,
            uwb_dist_right_m=2.0,
        )
        self.assertEqual(res["state"], "WALK_ASSIST")
        self.assertFalse(res["summon_active"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
