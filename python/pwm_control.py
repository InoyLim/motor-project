from datetime import datetime
from logging import log_event
# import serial # Don't need it for test

# ---------------------- CONFIG FOR CONDITIONS ------------------

temperature_max = 60.0
current_max = 1.9
system_status = "ON"

SEVERITY_NORMAL = "NORMAL"
SEVERITY_WARNING = "WARNING"
SEVERITY_CRITICAL = "CRITICAL"


# ---------------------- EVENT MAP ----------------------

EVENTS = {
    "critical_shutdown": {
        "message": "Shutdown! Power cutoff engaged.",
        "severity": SEVERITY_CRITICAL,
        "command": b'0',
    },
    "overcurrent_warning": {
        "message": "Overcurrent rectification measures engaged.",
        "severity": SEVERITY_WARNING,
        "command": b'2',
    },
    "overtemp_warning": {
        "message": "Overtemperature rectification measures engaged.",
        "severity": SEVERITY_WARNING,
        "command": b'3',
    },
    "normal_operation": {
        "message": "System is running healthy.",
        "severity": SEVERITY_NORMAL,
        "command": b'1',
    }
}


# ---------------------- EVENT FUNCTION ----------------------

def handle_event(event_name, current, temperature, ser):
    """
    Takes the event key (from EVENTS map), applies the appropriate
    command and logs it with all relevant parameters.
    """
    event = EVENTS[event_name]  # fetch parameters
    command = event["command"]

    ser.write(command)
    log_event(
        event=event["message"],
        severity=event["severity"],
        current=current,
        temperature=temperature,
        command=command
    )


# ---------------------- PWM CORE LOGIC ----------------------

def read_sensors():
    line = ser.readline().decode().strip()
    current, temp = map(float, line.split(","))
    print(f"Current: {current}A | Temp: {temp} C")


def control_motor_pwm(current, temperature, ser):
    if system_status != "ON":
        print("System is OFF")
        return

    if current >= current_max or temperature >= temperature_max:
        handle_event("critical_shutdown", current, temperature, ser)
    elif current >= 1.6:
        handle_event("overcurrent_warning", current, temperature, ser)
    elif temperature >= 55:
        handle_event("overtemp_warning", current, temperature, ser)
    else:
        handle_event("normal_operation", current, temperature, ser)


# ---------------------- READABILITY ----------------------

def send_motor_command(command):
    readable = {
        b'0': "System is at a dangerous threshold! The system will now kill power.\nCurrent & Temperature values at time of failure will be sent to the log.\n",
        b'1': "System is in Normal operations.",
        b'2': "System is engaging Load Regulation (Due to slight overcurrent).\nCurrent & Temperature values at time of event will be sent to the log.\n",
        b'3': "System is engaging Cooling Measures (Due to slight overtemperature).\nCurrent & Temperature values at time of event will be sent to the log.\n"
    }
    return readable.get(command, "Unknown command")


# ---------------------- MOCK HARDWARE / TEST ----------------------

class MockSerial:
    def __init__(self):
        self.commands = []

    def write(self, data):
        print(f"\nThe command-byte: {data} was sent to motor sensor.")
        self.commands.append(data)


# ---------------------- TEST CASES ----------------------

test_cases = [
    {"current": 1.4, "temperature": 40.0},
    {"current": 1.7, "temperature": 40.0},
    {"current": 1.4, "temperature": 55.0},
    {"current": 2.0, "temperature": 40.0},
    {"current": 1.5, "temperature": 60.0},
    {"current": 2.0, "temperature": 60.0},
]


case_index = int(input(
    "\nEntering Test mode. Simulate a motor condition.\n\n"
    "Which case would you like to test?\n"
    "Normal operations = 0\n"
    "Overcurrent = 1\n"
    "Overtemperature = 2\n"
    "Overcurrent beyond safety = 3\n"
    "Overtemperature beyond safety = 4\n"
    "Both beyond safety = 5\n"
    "Go through all test cases = 6\n\n"
))

ser = MockSerial()

if case_index == 6:
    for case in test_cases:
        control_motor_pwm(case['current'], case['temperature'], ser)
        last_command = ser.commands[-1]
        print("Readable command:", send_motor_command(last_command))
else:
    selected_case = test_cases[case_index]
    control_motor_pwm(selected_case['current'], selected_case['temperature'], ser)
    last_command = ser.commands[-1]
    print("This command means the motor status is:", send_motor_command(last_command))
