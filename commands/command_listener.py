def listen_for_command():
    # Replace this with VLM input or terminal input
    command = input("Enter command (f, left, right, stop): ").strip().lower()

    # If VLM integration is ready:
    # command = get_vlm_command()

    return command
