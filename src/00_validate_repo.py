import os

def validate_repo():
    print("Checking repository structure...\n")

    directories = ["data", "personas", "spec", "tests", "metrics", "src"]
    
    # All deliverables expected by the end of Task 6
    files_to_check = [
        "data/reviews_raw.jsonl",
        "data/reviews_clean.jsonl",
        "data/review_groups_auto.json",
        "data/review_groups_manual.json",
        "data/review_groups_hybrid.json",
        "personas/personas_manual.json",
        "personas/personas_auto.json",
        "personas/personas_hybrid.json",
        "spec/spec_manual.md",
        "spec/spec_auto.md",
        "spec/spec_hybrid.md",
        "tests/tests_manual.json",
        "tests/tests_auto.json",
        "tests/tests_hybrid.json",
        "metrics/metrics_manual.json",
        "metrics/metrics_auto.json",
        "metrics/metrics_hybrid.json",
        "metrics/metrics_summary.json",
        "src/run_all.py",
        "reflection/reflection.md",
        "README.md"
    ]

    all_passed = True

    # Check if folders exist
    for d in directories:
        if not os.path.isdir(d):
            print(f"Directory missing: {d}/")
            all_passed = False

    # Check if files exist
    for f in files_to_check:
        if os.path.isfile(f):
            print(f"{f} found")
        else:
            print(f"{f} MISSING")
            all_passed = False

    print("\nRepository validation complete.")
    if all_passed:
        print("Status: SUCCESS - All required files and folders are present!")
    else:
        print("Status: FAILED - Please make sure you have named all files correctly.")

if __name__ == "__main__":
    validate_repo()