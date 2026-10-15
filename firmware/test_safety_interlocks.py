#!/usr/bin/env python3
"""
Automated Verification Suite for ElderStep Pro Final 10.20 kg 5-Module Controller.
Verifies all 12 clinical, biomechanical, and autonomous safety laws:
  1. Dead-Man's Auto-Brake when hands leave forearm load cells
  2. Closed-Loop 12-Deg Inclined Column Synchronization (Left/Right Hall error correction)
  3. Maximum Perch Height Soft Limit Stop (713mm saddle / 873mm slide-bridge tray)
  4. IMU Tilt / Stumble Emergency Lock (>12 deg pitch/roll locks brakes and halts actuators)
  5. RT.Works RT.2 Slope-Zeroing Uphill Boost (+pitch increases hub torque automatically)
  6. RT.Works RT.2 Slope-Zeroing Downhill Braking (-pitch reduces hub speed to prevent runaway)
  7. Camino VL53L5CX Shin-Distance Runaway Guard (>28cm shin gap throttles speed to <=25 PWM)
  8. Zero-Turn Spin-in-Place Mode (Left wheel forward, Right wheel reverse in tight bathrooms)
  9. Auto-Summon Prep: Lowers seat <=350 pulses for low CG before autonomous rolling
 10. Auto-Summon UWB Differential Homing toward Grandma's Pendant
 11. Auto-Summon LiDAR Obstacle & Cliff Protection (<35cm obstacle or cliff locks brakes)
 12. Auto-Summon 50cm Docking + Instant Human-Grip Override
"""

import math
import unittest

LOAD_HANDS_PRESENT_THRESHOLD = 600
LOAD_PUSH_ASSIST_THRESHOLD   = 1400
MAX_PERCH_HEIGHT_PULSES      = 1200
SYNC_KP                      = 12
MAX_SAFE_TILT_DEG            = 12.0
SLOPE_COMP_GAIN              = 4.5
MAX_SAFE_SHIN_GAP_CM         = 28.0

SUMMON_STOP_DISTANCE_M       = 0.50
SUMMON_SLOWDOWN_DISTANCE_M   = 1.20
LIDAR_MIN_OBSTACLE_DIST_M    = 0.35
SUMMON_BASE_PWM              = 70
SUMMON_DOCK_PWM              = 38
SUMMON_TURN_KP               = 45


def evaluate_controller_step(
    load_left=0,
    load_right=0,
    pulses_left=0,
    pulses_right=0,
    btn_up=False,
    btn_down=False,
    btn_spin=False,
    btn_threshold=False,
    pitch_deg=0.0,
    roll_deg=0.0,
    shin_distance_cm=18.0,
    soft_start_pwm=220,
    summon_requested=False,
    uwb_dist_left_m=3.0,
    uwb_dist_right_m=3.0,
    lidar_front_obstacle_m=9.9,
    cliff_detected=False,
):
    avg_height = (pulses_left + pulses_right) // 2
    hands_on = (load_left > LOAD_HANDS_PRESENT_THRESHOLD) and (load_right > LOAD_HANDS_PRESENT_THRESHOLD)
    avg_force = (load_left + load_right) // 2

    # 0. IMU Tilt / Stumble Emergency Lock
    if abs(pitch_deg) > MAX_SAFE_TILT_DEG or abs(roll_deg) > MAX_SAFE_TILT_DEG:
        return {
            "state": "EMERGENCY_LOCK",
            "summon_active": False,
            "hub_brake_locked": True,
            "hub_l_pwm": 0,
            "hub_r_pwm": 0,
            "dir_l_fwd": True,
            "dir_r_fwd": True,
            "lift_l_pwm": 0,
            "lift_r_pwm": 0,
        }

    # Instant Human-Touch Override on Auto-Summon
    if hands_on and summon_requested:
        summon_requested = False

    # Autonomous Summon-to-Grandma
    if summon_requested and not hands_on:
        if cliff_detected or lidar_front_obstacle_m < LIDAR_MIN_OBSTACLE_DIST_M:
            return {
                "state": "AUTO_SUMMON_OBSTACLE_HOLD",
                "summon_active": True,
                "hub_brake_locked": True,
                "hub_l_pwm": 0,
                "hub_r_pwm": 0,
                "dir_l_fwd": True,
                "dir_r_fwd": True,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
            }
        if avg_height > 350:
            return {
                "state": "AUTO_SUMMON_PREP",
                "summon_active": True,
                "hub_brake_locked": True,
                "hub_l_pwm": 0,
                "hub_r_pwm": 0,
                "dir_l_fwd": True,
                "dir_r_fwd": True,
                "lift_l_pwm": 200,
                "lift_r_pwm": 200,
            }
        avg_dist = 0.5 * (uwb_dist_left_m + uwb_dist_right_m)
        if avg_dist <= SUMMON_STOP_DISTANCE_M:
            return {
                "state": "AUTO_SUMMON_DOCKED",
                "summon_active": False,
                "hub_brake_locked": True,
                "hub_l_pwm": 0,
                "hub_r_pwm": 0,
                "dir_l_fwd": True,
                "dir_r_fwd": True,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
            }
        baseline = 0.495
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
            "dir_l_fwd": True,
            "dir_r_fwd": True,
            "lift_l_pwm": 0,
            "lift_r_pwm": 0,
        }

    # 1. 12-Deg "Nose-Over-Toes" Sit-to-Stand Lift
    if btn_up or btn_down:
        if btn_up and avg_height >= MAX_PERCH_HEIGHT_PULSES:
            return {
                "state": "PERCH_MAX_HEIGHT_REACHED",
                "summon_active": False,
                "hub_brake_locked": True,
                "hub_l_pwm": 0,
                "hub_r_pwm": 0,
                "dir_l_fwd": True,
                "dir_r_fwd": True,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
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
            "dir_l_fwd": True,
            "dir_r_fwd": True,
            "lift_l_pwm": speed_l,
            "lift_r_pwm": speed_r,
        }

    # 2. Zero-Turn Spin-in-Place Mode
    if btn_spin and hands_on:
        return {
            "state": "SPIN_IN_PLACE",
            "summon_active": False,
            "hub_brake_locked": False,
            "hub_l_pwm": 55,
            "hub_r_pwm": 55,
            "dir_l_fwd": True,
            "dir_r_fwd": False,
            "lift_l_pwm": 0,
            "lift_r_pwm": 0,
        }

    # 3. Dead-Man's Auto-Brake & Walking Assist (with RT.2 Slope-Zeroing + Camino Shin Guard)
    if not hands_on or cliff_detected:
        return {
            "state": "PARKED_LOCKED",
            "summon_active": False,
            "hub_brake_locked": True,
            "hub_l_pwm": 0,
            "hub_r_pwm": 0,
            "dir_l_fwd": True,
            "dir_r_fwd": True,
            "lift_l_pwm": 0,
            "lift_r_pwm": 0,
        }

    hub_pwm = 0
    if btn_threshold:
        hub_pwm = 85
    elif avg_force > LOAD_PUSH_ASSIST_THRESHOLD:
        base_assist = int(40 + (avg_force - LOAD_PUSH_ASSIST_THRESHOLD) * (130 - 40) / (4095 - LOAD_PUSH_ASSIST_THRESHOLD))
        slope_comp = int(pitch_deg * SLOPE_COMP_GAIN)
        hub_pwm = max(0, min(160, base_assist + slope_comp))
        if shin_distance_cm > MAX_SAFE_SHIN_GAP_CM:
            hub_pwm = min(hub_pwm, 25)

    return {
        "state": "WALK_ASSIST",
        "summon_active": False,
        "hub_brake_locked": False,
        "hub_l_pwm": hub_pwm,
        "hub_r_pwm": hub_pwm,
        "dir_l_fwd": True,
        "dir_r_fwd": True,
        "lift_l_pwm": 0,
        "lift_r_pwm": 0,
    }


class TestElderStepFinal5ModuleController(unittest.TestCase):
    def test_01_dead_mans_auto_brake_when_hands_off(self):
        res = evaluate_controller_step(load_left=100, load_right=200)
        self.assertEqual(res["state"], "PARKED_LOCKED")
        self.assertTrue(res["hub_brake_locked"])

    def test_02_closed_loop_12deg_column_synchronization(self):
        res = evaluate_controller_step(pulses_left=205, pulses_right=200, btn_up=True, soft_start_pwm=200)
        self.assertEqual(res["state"], "SIT_TO_STAND_LIFT")
        self.assertLess(res["lift_l_pwm"], res["lift_r_pwm"])

    def test_03_perch_max_height_limit_stop(self):
        res = evaluate_controller_step(pulses_left=1200, pulses_right=1200, btn_up=True)
        self.assertEqual(res["state"], "PERCH_MAX_HEIGHT_REACHED")
        self.assertEqual(res["lift_l_pwm"], 0)

    def test_04_imu_stumble_emergency_lock(self):
        res = evaluate_controller_step(load_left=2500, load_right=2500, pitch_deg=14.5)
        self.assertEqual(res["state"], "EMERGENCY_LOCK")
        self.assertTrue(res["hub_brake_locked"])

    def test_05_rt2_slope_zeroing_uphill_boost_and_downhill_brake(self):
        flat = evaluate_controller_step(load_left=2500, load_right=2500, pitch_deg=0.0)
        uphill = evaluate_controller_step(load_left=2500, load_right=2500, pitch_deg=6.0)
        downhill = evaluate_controller_step(load_left=2500, load_right=2500, pitch_deg=-6.0)
        self.assertGreater(uphill["hub_l_pwm"], flat["hub_l_pwm"])
        self.assertLess(downhill["hub_l_pwm"], flat["hub_l_pwm"])

    def test_06_camino_shin_distance_runaway_guard(self):
        # When user's shins fall >28cm behind the walker, speed is throttled to <=25 PWM
        normal = evaluate_controller_step(load_left=3000, load_right=3000, shin_distance_cm=18.0)
        too_far = evaluate_controller_step(load_left=3000, load_right=3000, shin_distance_cm=34.0)
        self.assertGreater(normal["hub_l_pwm"], 60)
        self.assertLessEqual(too_far["hub_l_pwm"], 25)

    def test_07_zero_turn_spin_in_place_bathroom_mode(self):
        res = evaluate_controller_step(load_left=1500, load_right=1500, btn_spin=True)
        self.assertEqual(res["state"], "SPIN_IN_PLACE")
        self.assertTrue(res["dir_l_fwd"])
        self.assertFalse(res["dir_r_fwd"])

    def test_08_auto_summon_prep_lowers_high_saddle_before_rolling(self):
        res = evaluate_controller_step(summon_requested=True, pulses_left=600, pulses_right=600)
        self.assertEqual(res["state"], "AUTO_SUMMON_PREP")
        self.assertTrue(res["hub_brake_locked"])
        self.assertEqual(res["lift_l_pwm"], 200)

    def test_09_auto_summon_uwb_differential_steering_to_grandma(self):
        res = evaluate_controller_step(
            summon_requested=True,
            pulses_left=100,
            pulses_right=100,
            uwb_dist_left_m=2.00,
            uwb_dist_right_m=2.25,
        )
        self.assertEqual(res["state"], "AUTO_SUMMON_HOMING")
        self.assertGreater(res["hub_r_pwm"], res["hub_l_pwm"])

    def test_10_auto_summon_lidar_obstacle_and_cliff_protection(self):
        res = evaluate_controller_step(summon_requested=True, lidar_front_obstacle_m=0.22)
        self.assertEqual(res["state"], "AUTO_SUMMON_OBSTACLE_HOLD")
        self.assertTrue(res["hub_brake_locked"])

    def test_11_auto_summon_docks_and_locks_at_50cm(self):
        res = evaluate_controller_step(summon_requested=True, uwb_dist_left_m=0.48, uwb_dist_right_m=0.49)
        self.assertEqual(res["state"], "AUTO_SUMMON_DOCKED")
        self.assertTrue(res["hub_brake_locked"])

    def test_12_human_grip_instantly_overrides_auto_summon(self):
        res = evaluate_controller_step(load_left=1000, load_right=1000, summon_requested=True)
        self.assertEqual(res["state"], "WALK_ASSIST")
        self.assertFalse(res["summon_active"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
