import os
import subprocess
import time

def terminate_screen_session(session_name="mysession"):
    try:
        # Check if the screen session exists
        result = subprocess.run(["screen", "-ls"], capture_output=True, text=True)
        
        if session_name in result.stdout:
            print(f"Session '{session_name}' found. Terminating...")
            subprocess.run(["screen", "-S", session_name, "-X", "quit"], check=True)
            print(f"Session '{session_name}' terminated.")
        else:
            print(f"No session named '{session_name}' found.")
    except Exception as e:
        print(f"Error: {e}")

class ScreenTerminal:
    def __init__(self, session_name="mysession"):
        terminate_screen_session()
        self.session_name = session_name
        self.create_session()
        self.reference_processes = self.get_current_processes()

    def create_session(self):
        """Creates a new screen session if it does not exist."""
        subprocess.run(["screen", "-dmS", self.session_name], check=True)

    def send_command(self, command):
        """Sends a command to the screen session and waits for its completion."""
        subprocess.run(["screen", "-S", self.session_name, "-X", "stuff", command + ";" + "touch /tmp/done.txt\n"], check=True)
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
        #while True:
        #    current_processes = self.get_current_processes()
        #    if current_processes == self.reference_processes:
        #        break
        #    time.sleep(1)
        while not os.path.exists("/tmp/done.txt"):
            time.sleep(0.01)
            
        os.remove("/tmp/done.txt")

    def get_output(self):
        """Retrieves the latest output from the screen session."""
        try:
            result = subprocess.run(["screen", "-S", self.session_name, "-X", "hardcopy", "output.log"], check=True)
            time.sleep(1)  # Ensure output is written
            with open("output.log", "r", errors='ignore') as f:
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
    
    # Set and retrieve an environment variable
    terminal.send_command("export MY_VAR='Hello World'")
    terminal.send_command("echo $MY_VAR")
    output = terminal.get_output()
    print("MY_VAR:", output)
    
    

    terminal.send_command("pwd")
    output = terminal.get_output()
    print("Current Directory:", output)
    
#     Change directory and check if it persists
#    terminal.send_command("cd /tmp")
#    terminal.send_command("pwd")
#    output = terminal.get_output()
#    print("Current Directory:", output)
    
    # Create a file in the new directory and list it
    terminal.send_command("touch testfile.txt")
    terminal.send_command("ls -l")
    output = terminal.get_output()
    print("Files in Directory:", output)
    
    # Use an alias and check if it persists
    terminal.send_command("alias ll='ls -lah'")
    terminal.send_command("ll")
    output = terminal.get_output()
    print("Alias Output:", output)
    
    # Use an alias and check if it persists
  #  output = terminal.send_command("python3 ../../execution_agent_workspace/oss-fuzz/infra/helper.py build_image libtiff --no-pull")
  #  print("Python Output:", output)
  
    terminal.send_command("sdfdsfds 1>&2")
    output = terminal.get_output()
    print("Error Output:", output)
    
    terminal.send_command("python3 -u test.py")
    output = terminal.get_output()
    print("Test Output:", output)
    
    terminal.close_session()