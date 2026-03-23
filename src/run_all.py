import subprocess
import sys

def run_script(script_path, args=None):
    "Helper function to run a python script and handle errors."
    command = [sys.executable, script_path]
    if args:
        command.extend(args)
    
    print(f"\n---> Executing: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
        print(f"     [SUCCESS] {script_path} completed.")
    except subprocess.CalledProcessError as e:
        print(f"     [ERROR] Failed while executing {script_path}. Exiting pipeline.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"     [WARNING] {script_path} not found. Skipping...")

def main():
    print("Starting automated pipeline execution...\n")

    # 1. Data Cleaning
    run_script("src/02_clean.py")

    # 2. Automated Generation Steps
    # Runs the scripts intended to be generated programmatically
    run_script("src/05_personas_auto.py")
    run_script("src/06_spec_generate.py")
    run_script("src/07_tests_generate.py")

    # 3. Compute Metrics 
    # Generates the metrics files for comparison
    run_script("src/08_metrics.py", ["manual"])
    run_script("src/08_metrics.py", ["auto"])
    run_script("src/08_metrics.py", ["hybrid"])

    # STEP 4: Generate the Final Summary Table
    print("\nGenerating metrics summary...")
    run_script("src/09_summary.py")

    print("\n-----------------------------------------")
    print("Pipeline execution complete!")
    print("Check your metrics/ folder for the results.")
    print("-----------------------------------------\n")

if __name__ == "__main__":
    main()