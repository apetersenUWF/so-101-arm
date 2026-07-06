from python_st3215 import ST3215

port = "COM4" #place com port for servo connection here
original_id = 1
new_id = 2

controller = ST3215(port)
servo = controller.wrap_servo(original_id)
print(f"Attempting to change servo ID #{original_id} to ID #{new_id}")
servo.srarm.unlock()
if servo.eeprom.write_id(new_id):
    print("Success!")
else:
    print("Failure")
servo.sram.lock()