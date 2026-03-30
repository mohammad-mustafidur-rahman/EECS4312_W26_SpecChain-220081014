import subprocess
import sys
import json
import os

def run_script(script_path, args=None):
    """Helper function to run a python script and handle errors."""
    command = [sys.executable, script_path]
    if args:
        command.extend(args)

    print(f"\n---> Executing: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
        print(f"     [SUCCESS] {script_path} completed.")
    except subprocess.CalledProcessError:
        print(f"     [ERROR] Failed while executing {script_path}. Exiting pipeline.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"     [WARNING] {script_path} not found. Skipping...")

def generate_summary():
    """Generate metrics_summary.json and print comparison table."""
    pipelines = ["manual", "auto", "hybrid"]
    summary_data = {}

    print("\nGenerating metrics summary...\n")

    for p in pipelines:
        filepath = f"metrics/metrics_{p}.json"
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                summary_data[p] = json.load(f)
        else:
            print(f"[WARNING] {filepath} not found.")
            summary_data[p] = {}

    summary_filepath = "metrics/metrics_summary.json"

    with open(summary_filepath, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    print(f"[SUCCESS] Saved the results to {summary_filepath}\n")

    print("### Task 6: Performance Comparison Table\n")
    print("| Metric | Manual | Auto | Hybrid |")
    print("| :--- | :---: | :---: | :---: |")

    metrics_to_show = [
        ("dataset_size", "Dataset Size"),
        ("persona_count", "Persona Count"),
        ("requirements_count", "Requirements Count"),
        ("tests_count", "Tests Count"),
        ("traceability_links", "Traceability Links"),
        ("review_coverage", "Review Coverage"),
        ("traceability_ratio", "Traceability Ratio"),
        ("testability_rate", "Testability Rate"),
        ("ambiguity_ratio", "Ambiguity Ratio"),
    ]

    for key, label in metrics_to_show:
        row = f"| **{label}** "
        for p in pipelines:
            val = summary_data.get(p, {}).get(key, "N/A")
            if isinstance(val, float):
                row += f"| {val:.4f} "
            else:
                row += f"| {val} "
        row += "|"
        print(row)

def main():
    print("Starting automated pipeline execution...\n")

    # 1. Data Cleaning
    run_script("src/02_clean.py")

    # 2. Automated Generation Steps
    run_script("src/05_personas_auto.py")
    run_script("src/06_spec_generate.py")
    run_script("src/07_tests_generate.py")

    # 3. Compute Metrics
    run_script("src/08_metrics.py", ["manual"])
    run_script("src/08_metrics.py", ["auto"])
    run_script("src/08_metrics.py", ["hybrid"])

    # 4. Update metrics_summary.json
    generate_summary()

    print("\n-----------------------------------------")
    print("Pipeline execution complete!")
    print("-----------------------------------------\n")

if __name__ == "__main__":
    main()