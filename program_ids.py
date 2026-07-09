from python_st3215 import ST3215

port = "COM6" #place com port for servo connection here
original_id = 1
new_id = 6

controller = ST3215(port)
servo = controller.wrap_servo(original_id)
print(f"Attempting to change servo ID #{original_id} to ID #{new_id}")
servo.sram.unlock()
servo.eeprom.write_id(new_id)
servo.sram.lock()
new_servo = controller.wrap_servo(new_id)
if new_servo.ping() is None:
    print("Failure")
else:
    print("Success!")
print(f"New ID #{new_servo.eeprom.read_id()}")


