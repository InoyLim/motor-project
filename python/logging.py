from datetime import datetime

def log_event(message):
    with open("motor_log.txt", "a") as f:
        f.write(f"{datetime.now()} - {message}\n")