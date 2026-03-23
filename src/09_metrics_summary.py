import json
import os

def generate_summary():
    # The three pipelines we are tracking
    pipelines = ["manual", "auto", "hybrid"]
    summary_data = {}

    print("Generating metrics summary...\n")

    # 1. Load each individual metrics file
    for p in pipelines:
        filepath = f"metrics/metrics_{p}.json"
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                # Store the data under the pipeline's name
                summary_data[p] = json.load(f)
        else:
            print(f"[WARNING] {filepath} not found. Make sure to run 08_metrics.py {p} first.")
            summary_data[p] = {} # Create an empty dictionary so the script doesn't crash

    # 2. Save the consolidated metrics_summary.json
    os.makedirs("metrics", exist_ok=True)
    summary_filepath = "metrics/metrics_summary.json"
    
    with open(summary_filepath, "w") as f:
        json.dump(summary_data, f, indent=2)
    
    print(f"[SUCCESS] Saved consolidated results to {summary_filepath}\n")

    # 3. Generate a Markdown Table for the terminal
    print("### Task 6: Performance Comparison Table\n")
    
    header = "| Metric | Manual | Auto | Hybrid |"
    separator = "| :--- | :---: | :---: | :---: |"
    print(header)
    print(separator)

    metrics_to_show = [
        ("dataset_size", "Dataset Size"),
        ("persona_count", "Persona Count"),
        ("requirements_count", "Requirements Count"),
        ("tests_count", "Tests Count"),
        ("traceability_links", "Traceability Links"),
        ("review_coverage", "Review Coverage"),
        ("traceability_ratio", "Traceability Ratio"),
        ("testability_rate", "Testability Rate"),
        ("ambiguity_ratio", "Ambiguity Ratio")
    ]

    for key, label in metrics_to_show:
        row = f"| **{label}** "
        for p in pipelines:
            val = summary_data.get(p, {}).get(key, "N/A")
            
            # Format floating point numbers nicely (like 0.0108 instead of 0.010799999)
            if isinstance(val, float):
                row += f"| {val:.4f} "
            else:
                row += f"| {val} "
        row += "|"
        print(row)
    
if __name__ == "__main__":
    generate_summary()