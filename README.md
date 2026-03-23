# EECS4312_W26_SpecChain

Application: MindDoc: Your Clinical Companion

Dataset:
- Data Collection Method: Automated scraping from the Google Play Store.
- reviews_raw.jsonl contains the initially collected raw reviews.
- reviews_clean.jsonl contains the pre-processed and filtered dataset.
- The cleaned dataset contains 2,584 reviews.

Repository Structure:
- data/ contains the raw/cleaned datasets and the thematic review group JSON files.
- personas/ contains the manual, auto, and hybrid persona definitions.
- spec/ contains the Markdown software requirement specifications.
- tests/ contains the validation test cases linked to the requirements.
- metrics/ contains all pipeline metric calculations and the final summary comparison.
- src/ contains the executable Python scripts for the automated pipeline.
- reflection/ contains the final Task 8 project reflection.

How to Run:
1. python3 src/00_validate_repo.py
2. python3 src/run_all.py
3. Open metrics/metrics_summary.json to view the pipeline comparison results.