VALID_COMMANDS = ['forward', 'left', 'right', 'stop']

def parse_command(command_str):
    """
    Parse and validate the input command string.
    Returns a normalized command or None if invalid.
    """
    command = command_str.strip().lower()
    if command in VALID_COMMANDS:
        return command
    return None
