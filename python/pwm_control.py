from datetime import datetime
from logging import log_event
# import serial # Don't need it for test


temperature_max = 60.0 # maximum values set locally
current_max = 1.9 
system_status = "ON"

temperature = 0.0
current = 0.0

SEVERITY_NORMAL = "NORMAL"
SEVERITY_WARNING = "WARNING"
SEVERITY_CRITICAL = "CRITICAL"



def read_sensors(): # this will read the data from the sensors
    line = ser.readline().decode().strip() # we are calling data from arduino
    current, temp = map(float, line.split(",")) # we are attributing the raw values from arduino to current and temp e.g. 1.2 , 60.2
    print(f"Current: {current}A | Temp: {temp} C") 


def control_motor_pwm(current, temperature, ser): # max current arbitrarily to 1.9
    if system_status == "ON":
        if current >= current_max or temperature >= temperature_max:
            ser.write(b'0') # byte '0' means cut off all power
            log_event(
                event="Shutdown!",
                severity=SEVERITY_CRITICAL,
                current=current,
                temperature=temperature,
                command=b'0')
        
        elif current >= 1.6: #overcurrent warning
            ser.write(b'2') # '2' load regulation, reduce voltage,
            log_event(
                event="Overcurrent rectification measures engaged",
                severity=SEVERITY_WARNING,
                current=current,
                temperature=temperature,
                command=b'2')
        
        elif temperature >= 55: #overtemperature warning
            ser.write(b'3') # '3' turning on cooling fan, reduce temperature
            log_event(
                event="Overtemperature rectification measures engaged",
                severity=SEVERITY_WARNING,
                current=current,
                temperature=temperature,
                command=b'3')
        
        else:
            ser.write(b'1') # '1' normal operations   
            log_event(
                event="System is running healthy",
                severity=SEVERITY_NORMAL,
                current=current,
                temperature=temperature,
                command=b'1')
    
    else:
        print("System is OFF")


def send_motor_command(command):
    readable = {
        b'0': "System is at a dangerous threshold! The system will now kill power.\nCurrent & Temperature values at time of failure will be sent to the log.\n",
        b'1': "System is in Normal operations.",
        b'2': "System is engaging Load Regulation (Due to slight overcurrent).\nCurrent & Temperature values at time of event will be sent to the log.\n",
        b'3': "System is engaging Cooling Measures (Due to slight overtemperature).\nCurrent & Temperature values at time of event will be sent to the log.\n"   
    }
    return readable.get(command, "Unknown command")



class MockSerial: # We are defining a class that mimics how Arduino may behave
    def __init__(self):
        self.commands = [] #This is where we store the commands
    
    def write(self, data):
        print(f"\nThe command-byte: {data} was sent to motor sensor.")
        self.commands.append(data)


 
test_cases = [
    {"current": 1.4, "temperature": 40.0 }, # normal
    {"current": 1.7, "temperature": 40.0 }, # over current - warning
    {"current": 1.4, "temperature": 55.0 }, # over temp - warning
    {"current": 2.0, "temperature": 40.0 }, # over current - DANGER
    {"current": 1.5, "temperature": 60.0 }, # over temp - DANGER
    {"current": 2.0, "temperature": 60.0 }, # both DANGER
]


case_index = int(input( # added testing functionality
    "\n"
    "Entering Test mode. The purpose of this mode is to simualte a motor condition.\n"
    "\n"
    "When you send a test condition, the controller will respond as if those readings came from real sensors -\n"
    "\n"
    "We should expect that, upon reading varying conditions, it issues the corresponding control command\n"
    "\n"
    "[Example]: You input '3' = The system is simulating overcurrent beyond what is reasonably safe.\n"
    "The system then sends a command-byte '0', to the sensor.\n"
    "When operational, this byte is read by the sensor and corresponds to mean = Shut off operations immediately!\n"
    "This then logs the data onto our 'motor_log.txt' with date and time stamp."
    "\n"
    "\n"
    "Which case would you like to test?\n"
    "\n"
    "Normal operations = 0\n" 
    "Overcurrent = 1\n"
    "Overtemperature = 2\n"
    "Overcurrent beyond safety = 3\n"
    "Overtemperature beyond safety = 4\n"
    "Both beyond safety = 5\n"
    "Go through the test cases = 6\n"
    "\n"
    ))



ser = MockSerial()

if case_index == 6:
    # run all test cases 
    for case in test_cases:
        control_motor_pwm(case['current'], case['temperature'], ser)
        last_command = ser.commands[-1] # last command sent to the motor
        print ("Readable command:", send_motor_command(last_command))
else:
    # run a single test case
    selected_case = test_cases[case_index]
    control_motor_pwm(selected_case['current'], selected_case['temperature'], ser)
    last_command = ser.commands[-1]
    print("This command means the motor status is:", send_motor_command(last_command))



