from datetime import datetime
from typing import Optional

# Clear the log file when the system starts
open("motor_log.txt", "w").close()

def log_event(
    event: str,
    severity: str = "INFO",
    current: Optional[float] = None,
    temperature: Optional[float] = None,
    command: Optional[bytes] = None
):
    """
    Logs a structured event entry to motor_log.txt.
    Each event includes timestamp, severity, sensor values, and command byte.
    """
    with open("motor_log.txt", "a") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        # Format numerical and byte data for readability
        current_str = f"{current:.2f} A" if current is not None else "N/A"
        temp_str = f"{temperature:.2f} C" if temperature is not None else "N/A"
        command_str = (
            f"{command.decode()}" if isinstance(command, bytes)
            else str(command) if command is not None else "N/A"
        )

        # Structured output
        log.write(
            f"[{timestamp}] EVENT = {event} | "
            f"SEVERITY = {severity} | "
            f"CURRENT = {current_str} | "
            f"TEMP = {temp_str} | "
            f"COMMAND = Command byte '{command_str}' sent to Arduino.\n"
        )
