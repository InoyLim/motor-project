from datetime import datetime
from typing import Optional

# clears the log file when the system starts
open("motor_log.txt", "w").close()

def log_event(
    event: str,
    severity: str = "INFO",
    current: Optional[float] = None,
    temperature: Optional[float] = None,
    command: Optional[bytes] = None
):
    with open("motor_log.txt", "a") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        current_str = f"{current:.2f} A" if current is not None else "N/A"
        temp_str = f"{temperature:.2f} C" if temperature is not None else "N/A"
        command_str = command.decode() if isinstance(command, bytes) else str(command)

        log.write(
            f"[{timestamp}] EVENT = {event} | SEVERITY = {severity} | "
            f"CURRENT = {current_str} | TEMP = {temp_str} | COMMAND = Command byte '{command_str}' Sent to arduino.\n"
        )


