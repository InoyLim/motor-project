""" Placeholder

import arduino_interface
import temperature_sensore
from gpiozero import PWMOutputDevice
import serial
from datetime import datetime

"""
from datetime import datetime

def log_event(message):
    with open("motor_log.txt", "a") as f:
        f.write(f"{datetime.now()} - {message}\n")



temperature_max = 60.0 # maximum values set locally
current_max = 1.9 
system_status = "ON"

temperature = 0.0
current = 0.0

test_cases = [
    {"current": 1.4, "temperature": 40.0 }, # normal
    {"current": 1.7, "temperature": 40.0 }, # over current - warning
    {"current": 1.4, "temperature": 55.0 }, # over temp - warning
    {"current": 2.0, "temperature": 40.0 }, # over current - DANGER
    {"current": 1.5, "temperature": 60.0 }, # over temp - DANGER
    {"current": 2.0, "temperature": 60.0 }, # both DANGER
]

for case in test_cases:
    current = case["current"]
    temperature = case["temperature"]

    if system_status == "ON":
        if current >= 1.8 or temperature >= 60: #full shutdown
            print(f"Shutdown! Current: {current}, Temp: {temperature}")
        elif current >= 1.6: #overcurrent warning
            print(f"Overcurrent rectification measures engaged - Current: {current}, Temp: {temperature}")
        elif temperature >= 55: #overtemperature warning
            print(f"Overtemperature rectification measures engaged - Current: {current}, Temp: {temperature}")
        else: #running normally
            print(f"System running normally Current: {current}, Temp: {temperature}")
    else:
        print("System is OFF")

for case in test_cases:
    current = case["current"]
    temperature = case["temperature"]
    
    if system_status == "ON":
        if current >= 1.8 or temperature >= 60: #full shutdown
            log_event(f"Shutdown! Current: {current}, Temp: {temperature}")
        elif current >= 1.6: #overcurrent warning
            log_event(f"Overcurrent rectification measures engaged - Current: {current}, Temp: {temperature}")
        elif temperature >= 55: #overtemperature warning
            log_event(f"Overtemperature rectification measures engaged - Current: {current}, Temp: {temperature}")
        else: #running normally
            log_event(f"System running normally Current: {current}, Temp: {temperature}")
    else:
        print("System is OFF")






""" Placeholder
def read_sensors(): # this will read the data from the sensors
    line = ser.readline().decode().strip() # we are calling data from arduino
    current, temp = map(float, line.split(",")) # we are attributing the raw values from arduino to current and temp e.g. 1.2 , 60.2
    print(f"Current: {current}A | Temp: {temp} C") 
"""

"""
def control_motor_pwm(current, temperature): # max current arbitrarily to 1.6
    if system_status == "ON":
        if current > 1.6 or temperature > 60:
            ser.write(b'0') # byte '0' means cut off all power
            log_event("Overcurrent detected, shutting down operation")
        elif temperature > 40:
            ser.write(b'1') # '1' load regulation, reduce voltage,
            log_event("Motor is running hot, cooling fan turned on")
        elif temperature > 50: 
        else:
            ser.write(b'2') # '2' normal operations

"""

    