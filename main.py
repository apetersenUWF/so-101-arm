import time

from python_st3215 import ST3215

PORT = 'COM6'

target_angles = [2048 - 512, 2048, 2048, 2048 + 1024, 2048, 2048]
with ST3215(PORT) as controller:
    servo_ids = controller.list_servos()
    if servo_ids == [1, 2, 3, 4, 5, 6]:
        servos = []
        for i in servo_ids:
           servos.append(controller.wrap_servo(i))
        for i in range(len(servos)):
            servos[i].sram.torque_enable()
            servos[i].sram.write_acceleration(5)
        for i in range(len(servos)):
            servos[i].sram.write_target_location(target_angles[i])
            time.sleep(0.2)
        time.sleep(5)
        for servo in servos:
            servo.sram.torque_disable()