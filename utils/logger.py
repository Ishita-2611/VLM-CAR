import datetime

def log(message):
    """
    Simple logger to print messages with timestamps.
    """
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{time_stamp}] {message}")
