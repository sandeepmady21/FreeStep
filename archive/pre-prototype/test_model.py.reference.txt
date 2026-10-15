#!/usr/bin/env python3
"""
Automated Verification Suite for FreeStep Air (9.65 kg Clinical & Home Mastery Edition).
Verifies all 16 clinical, biomechanical, rehab-biofeedback, and safety laws:
  1. Dead-Man's Auto-Brake when hands leave forearm trough sensors
  2. Closed-Loop 12-Deg Inclined Column Synchronization (Left/Right Hall error correction)
  3. Maximum Perch Height Soft Limit Stop (713mm saddle / 873mm forearm halo)
  4. IMU Tilt / Stumble Emergency Lock (>12 deg pitch/roll locks brakes and halts actuators)
  5. RT.Works RT.2 Slope-Zeroing Uphill Boost (+pitch increases hub torque automatically)
  6. RT.Works RT.2 Slope-Zeroing Downhill Braking (-pitch reduces hub speed to prevent runaway)
  7. Camino VL53L1X Shin-Distance Runaway Guard (>28cm shin gap throttles speed to <=25 PWM)
  8. Zero-Turn Spin-in-Place Mode (Left wheel forward, Right wheel reverse in tight bathrooms)
  9. Auto-Summon / Valet Fetch Prep: Lowers seat <=350 pulses for low CG before rolling
 10. Differential Homing / Steering toward User
 11. ToF / LiDAR Obstacle & Cliff Protection (<35cm obstacle or cliff locks brakes)
 12. 50cm Docking + Instant Human-Grip Override
 13. Seated Power-Glide Mode (0.25 m/s indoor glide through 20" bathroom doors when seated + latched + thumb switch held; instant lock on release)
 14. 90-Deg Single-Leg Knee-Scooter Mode (caps height <=320 pulses / 480mm knee rest for 100% weight-free ankle fracture mobility)
 15. Graduated Weight-Bearing (PWB) Rehab Coach (biofeedback alert when forearm trough offload < prescribed target kg)
 16. Wristband Remote 'Valet Park-Away' + Automatic 2:00 AM PIR Motion Under-Frame Nightlight
"""

import math
import unittest

LOAD_HANDS_PRESENT_THRESHOLD = 600
LOAD_PUSH_ASSIST_THRESHOLD   = 1400
MAX_PERCH_HEIGHT_PULSES      = 1200
MAX_KNEE_SCOOTER_PULSES      = 320
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
    btn_seated_glide=False,
    seat_occupied=False,
    latch_locked=True,
    knee_scooter_90deg=False,
    pwb_target_offload_kg=0.0,
    valet_park_away=False,
    pir_night_motion=False,
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

    # Convert ADC forearm trough reading (0..4095) to kg offloaded by left+right forearms (0..60 kg full scale)
    forearm_offload_kg = round(((load_left + load_right) / 8190.0) * 60.0, 2)
    pwb_overload_alert = (pwb_target_offload_kg > 0.0) and hands_on and (forearm_offload_kg < pwb_target_offload_kg)
    nightlight_pwm = 180 if (pir_night_motion or hands_on) else 0

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
            "forearm_offload_kg": forearm_offload_kg,
            "pwb_overload_alert": pwb_overload_alert,
            "nightlight_pwm": nightlight_pwm,
        }

    # Instant Human-Touch Override on Auto-Summon / Valet
    if hands_on and (summon_requested or valet_park_away):
        summon_requested = False
        valet_park_away = False

    # Valet Park-Away Mode (backs walker neatly toward bedroom wall after user sits on bed/sofa)
    if valet_park_away and not hands_on and not seat_occupied:
        if cliff_detected or lidar_front_obstacle_m < LIDAR_MIN_OBSTACLE_DIST_M:
            return {
                "state": "VALET_PARKED_AT_WALL",
                "summon_active": False,
                "hub_brake_locked": True,
                "hub_l_pwm": 0,
                "hub_r_pwm": 0,
                "dir_l_fwd": False,
                "dir_r_fwd": False,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
                "forearm_offload_kg": forearm_offload_kg,
                "pwb_overload_alert": False,
                "nightlight_pwm": nightlight_pwm,
            }
        return {
            "state": "VALET_PARKING_REVERSE",
            "summon_active": True,
            "hub_brake_locked": False,
            "hub_l_pwm": 40,
            "hub_r_pwm": 40,
            "dir_l_fwd": False,
            "dir_r_fwd": False,
            "lift_l_pwm": 0,
            "lift_r_pwm": 0,
            "forearm_offload_kg": forearm_offload_kg,
            "pwb_overload_alert": False,
            "nightlight_pwm": nightlight_pwm,
        }

    # Autonomous / Valet Fetch-to-User
    if summon_requested and not hands_on and not seat_occupied:
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
                "forearm_offload_kg": forearm_offload_kg,
                "pwb_overload_alert": False,
                "nightlight_pwm": nightlight_pwm,
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
                "forearm_offload_kg": forearm_offload_kg,
                "pwb_overload_alert": False,
                "nightlight_pwm": nightlight_pwm,
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
                "forearm_offload_kg": forearm_offload_kg,
                "pwb_overload_alert": False,
                "nightlight_pwm": nightlight_pwm,
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
            "forearm_offload_kg": forearm_offload_kg,
            "pwb_overload_alert": False,
            "nightlight_pwm": nightlight_pwm,
        }

    # 1. 12-Deg "Nose-Over-Toes" Sit-to-Stand Lift (with 90° Knee-Scooter Height Cap)
    if btn_up or btn_down:
        max_allowed = MAX_KNEE_SCOOTER_PULSES if knee_scooter_90deg else MAX_PERCH_HEIGHT_PULSES
        if btn_up and avg_height >= max_allowed:
            return {
                "state": "KNEE_SCOOTER_MAX_HEIGHT" if knee_scooter_90deg else "PERCH_MAX_HEIGHT_REACHED",
                "summon_active": False,
                "hub_brake_locked": True,
                "hub_l_pwm": 0,
                "hub_r_pwm": 0,
                "dir_l_fwd": True,
                "dir_r_fwd": True,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
                "forearm_offload_kg": forearm_offload_kg,
                "pwb_overload_alert": pwb_overload_alert,
                "nightlight_pwm": nightlight_pwm,
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
            "forearm_offload_kg": forearm_offload_kg,
            "pwb_overload_alert": pwb_overload_alert,
            "nightlight_pwm": nightlight_pwm,
        }

    # 2. Seated Occupancy Mode: Auto-Lock Hold vs. Seated Power-Glide (0.25 m/s through 20" bathroom doors)
    if seat_occupied:
        if latch_locked and hands_on and btn_seated_glide and not cliff_detected:
            return {
                "state": "SEATED_POWER_GLIDE",
                "summon_active": False,
                "hub_brake_locked": False,
                "hub_l_pwm": 45,
                "hub_r_pwm": 45,
                "dir_l_fwd": True,
                "dir_r_fwd": True,
                "lift_l_pwm": 0,
                "lift_r_pwm": 0,
                "forearm_offload_kg": forearm_offload_kg,
                "pwb_overload_alert": False,
                "nightlight_pwm": nightlight_pwm,
            }
        return {
            "state": "SEATED_LOCKED_HOLD",
            "summon_active": False,
            "hub_brake_locked": True,
            "hub_l_pwm": 0,
            "hub_r_pwm": 0,
            "dir_l_fwd": True,
            "dir_r_fwd": True,
            "lift_l_pwm": 0,
            "lift_r_pwm": 0,
            "forearm_offload_kg": forearm_offload_kg,
            "pwb_overload_alert": False,
            "nightlight_pwm": nightlight_pwm,
        }

    # 3. Zero-Turn Spin-in-Place Mode
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
            "forearm_offload_kg": forearm_offload_kg,
            "pwb_overload_alert": pwb_overload_alert,
            "nightlight_pwm": nightlight_pwm,
        }

    # 4. Dead-Man's Auto-Brake & Walking Assist (with RT.2 Slope-Zeroing + Camino Shin Guard + PWB Rehab Coach)
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
            "forearm_offload_kg": forearm_offload_kg,
            "pwb_overload_alert": False,
            "nightlight_pwm": nightlight_pwm,
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
        "state": "KNEE_SCOOTER_GLIDE" if knee_scooter_90deg else "WALK_ASSIST",
        "summon_active": False,
        "hub_brake_locked": False,
        "hub_l_pwm": hub_pwm,
        "hub_r_pwm": hub_pwm,
        "dir_l_fwd": True,
        "dir_r_fwd": True,
        "lift_l_pwm": 0,
        "lift_r_pwm": 0,
        "forearm_offload_kg": forearm_offload_kg,
        "pwb_overload_alert": pwb_overload_alert,
        "nightlight_pwm": nightlight_pwm,
    }


class TestFreeStepAirFinal5ModuleController(unittest.TestCase):
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

    def test_13_seated_power_glide_through_narrow_bathroom_door(self):
        # Seated without pressing thumb switch -> locked solid
        locked = evaluate_controller_step(seat_occupied=True, latch_locked=True, load_left=1200, load_right=1200, btn_seated_glide=False)
        self.assertEqual(locked["state"], "SEATED_LOCKED_HOLD")
        self.assertTrue(locked["hub_brake_locked"])
        # Seated + latched + holding forearm troughs + pressing thumb glide switch -> smooth 45 PWM indoor glide!
        gliding = evaluate_controller_step(seat_occupied=True, latch_locked=True, load_left=1200, load_right=1200, btn_seated_glide=True)
        self.assertEqual(gliding["state"], "SEATED_POWER_GLIDE")
        self.assertFalse(gliding["hub_brake_locked"])
        self.assertEqual(gliding["hub_l_pwm"], 45)

    def test_14_90deg_single_leg_knee_scooter_mode(self):
        # Caps height at 320 pulses (480mm knee rest) and enables KNEE_SCOOTER_GLIDE
        cap = evaluate_controller_step(knee_scooter_90deg=True, pulses_left=320, pulses_right=320, btn_up=True)
        self.assertEqual(cap["state"], "KNEE_SCOOTER_MAX_HEIGHT")
        glide = evaluate_controller_step(knee_scooter_90deg=True, load_left=2000, load_right=2000)
        self.assertEqual(glide["state"], "KNEE_SCOOTER_GLIDE")
        self.assertGreater(glide["hub_l_pwm"], 40)

    def test_15_graduated_pwb_rehab_coach_biofeedback(self):
        # Doctor prescribes >=25 kg forearm offload to protect healing ankle
        overloaded_ankle = evaluate_controller_step(load_left=1200, load_right=1200, pwb_target_offload_kg=25.0)
        self.assertTrue(overloaded_ankle["pwb_overload_alert"])
        proper_offload = evaluate_controller_step(load_left=2200, load_right=2200, pwb_target_offload_kg=25.0)
        self.assertFalse(proper_offload["pwb_overload_alert"])
        self.assertGreaterEqual(proper_offload["forearm_offload_kg"], 25.0)

    def test_16_valet_park_away_and_2am_motion_nightlight(self):
        park = evaluate_controller_step(valet_park_away=True, pir_night_motion=True)
        self.assertEqual(park["state"], "VALET_PARKING_REVERSE")
        self.assertFalse(park["dir_l_fwd"])
        self.assertEqual(park["nightlight_pwm"], 180)


if __name__ == "__main__":
    unittest.main(verbosity=2)
