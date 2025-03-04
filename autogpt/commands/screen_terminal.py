import subprocess
import time

class ScreenTerminal:
    def __init__(self, session_name="mysession"):
        self.session_name = session_name
        self.create_session()
        self.reference_processes = self.get_current_processes()

    def create_session(self):
        """Creates a new screen session if it does not exist."""
        subprocess.run(["screen", "-dmS", self.session_name], check=True)

    def send_command(self, command):
        """Sends a command to the screen session and waits for its completion."""
        subprocess.run(["screen", "-S", self.session_name, "-X", "stuff", command + "\n"], check=True)
        time.sleep(1)  # Give time for the command to execute
        self.wait_for_completion()

    def get_current_processes(self):
        """Gets the current list of running processes."""
        try:
            result = subprocess.run(["ps", "-ef"], capture_output=True, text=True, check=True)
            return set(result.stdout.split("\n"))
        except subprocess.CalledProcessError as e:
            print("Error retrieving processes:", e)
            return set()

    def wait_for_completion(self):
        """Waits for the command to finish executing by checking process differences."""
        while True:
            current_processes = self.get_current_processes()
            if current_processes == self.reference_processes:
                break
            time.sleep(1)

    def get_output(self):
        """Retrieves the latest output from the screen session."""
        try:
            result = subprocess.run(["screen", "-S", self.session_name, "-X", "hardcopy", "output.log"], check=True)
            time.sleep(1)  # Ensure output is written
            with open("output.log", "r") as f:
                return f.read()
        except Exception as e:
            return f"Error retrieving output: {e}"

    def close_session(self):
        """Closes the screen session."""
        subprocess.run(["screen", "-S", self.session_name, "-X", "quit"], check=True)

# Example Usage
if __name__ == "__main__":
    terminal = ScreenTerminal()
    terminal.send_command("echo Hello, Screen!")
    output = terminal.get_output()
    print("Command Output:", output)
    terminal.close_session()
