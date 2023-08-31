import subprocess
import sys

def run_script(script_path, num_times):
    for _ in range(num_times):
        result = subprocess.run([sys.executable, script_path])
        if result.returncode != 0:
            print(f"Error occurred when running {script_path}. Stopping further runs.")
            break
        else:
            print(f"Completed run {_ + 1} of {script_path}.")

if __name__ == "__main__":
    script_to_run = "mockdata2.py"  # Replace with the path to your script
    times_to_run = 500  # Adjust as needed

    run_script(script_to_run, times_to_run)
