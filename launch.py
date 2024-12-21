import subprocess

def start_terminal(command, title=""):
    """Start a command in a new terminal window."""
    try:
        subprocess.Popen(f'start cmd /k "{command}"', shell=True)
    except:
        raise RuntimeError(f"Application Only Compatible with Windows")

if __name__ == "__main__":
    # Commands to run the publisher and subscriber
    pub_command = "python publisher.py"
    sub_command = "python subscriber.py"

    # Start the publisher in a new terminal
    print("Launching Publisher...")
    start_terminal(pub_command, title="Publisher")

    # Start the subscriber in another terminal
    print("Launching Subscriber...")
    start_terminal(sub_command, title="Subscriber")
