from python_st3215 import ST3215
from python_st3215.errors import ChecksumError
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
        for i in range(len(servos)):
            servos[i].sram.torque_disable()
            servos[i].sram.unlock()
        for i in range(len(servos), len(servos)):
            print(f"Move ({servo_names[i]}) to the middle of its range of motion")
            confirm = input("Press enter to confirm location")
            servos[i].sram.correct_position_to_2048()
            print(f"({servo_names[i]}) midpoint succesfully updated!")
            print(f"Move ({servo_names[i]}) to the minimum point in its range of motion")
            time.sleep(2)
            print("Begin!")
            for j in range(50):
                try:
                    position = servos[i].sram.read_current_location()
                    print(position)
                except (ChecksumError):
                    pass
                time.sleep(0.1)
            confirm2 = input(f"When ({servo_names[i]}) is in the minimum point in its range of motion press enter")
            servos[i].eeprom.write_min_angle_limit(servos[i].sram.read_current_location())
            print(f"Move ({servo_names[i]}) to the maximum point in its range of motion")
            time.sleep(2)
            print("Begin!")
            for j in range(50):
                try:
                    position = servos[i].sram.read_current_location()
                    print(position)
                except (ChecksumError):
                    pass
                time.sleep(0.1)
            confirm2 = input(f"When ({servo_names[i]}) is in the maximum point in its range of motion press enter")
            servos[i].eeprom.write_max_angle_limit(servos[i].sram.read_current_location())
        print("Servo, Min, Current, Max")
        for i in range(len(servos)):
            min = servos[i].eeprom.read_min_angle_limit()
            current_loc = servos[i].sram.read_current_location()
            max = servos[i].eeprom.read_max_angle_limit()
            print(f"({servo_names[i]}) {min} {current_loc} {max}")
            servos[i].sram.lock()
