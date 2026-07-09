from python_st3215 import ST3215
import time
PORT = 'COM6'
servo_names = ['base', 'shoulder', 'upper_arm', 'lower_arm', 'wrist', 'gripper']
with ST3215(PORT) as controller:
    servo_ids = controller.list_servos()
    if servo_ids != [1, 2, 3, 4, 5, 6]:
        print("Some servos were not detected, verify connections and try again.")
        print(f"Detected servo id's: [{servo_ids}]")
    else:
        servos = []
        for servo_id in servo_ids:
            servos.append(controller.wrap_servo(servo_id))
        while True:
            current_positions = []
            for servo in servos:
                current_positions.append(servo.sram.read_current_location())
            for i in range(len(servo_names)):
                print(f"{servo_names[i]} current position: {current_positions[i]}")
            time.sleep(0.5)