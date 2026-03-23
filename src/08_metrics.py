import json
import os
import re
import sys
from collections import defaultdict

AMBIGUOUS_TERMS = [
    "fast", "faster", "quick", "quickly", "easy", "easier", "simple", "simply",
    "better", "best", "good", "great", "seamless", "smooth", "efficient",
    "efficiently", "user-friendly", "friendly", "intuitive", "convenient",
    "helpful", "robust", "reliable", "flexible", "optimize", "optimized",
    "improve", "improved", "sufficient", "appropriate"
]

RECOGNIZED_FIELDS = {
    "req_id": ["Requirement ID"],
    "description": ["Description", "Requirement", "System Behavior"],
    "persona": ["Originating Persona", "Persona ID", "Persona", "Motivated By", "Source Persona"],
    "review_group": ["Traceability to Review Group", "Review Group ID", "Review Group", "Traceability", "Source Group"],
    "acceptance": ["Acceptance Criteria", "Acceptance Criterion"],
}


def load_json_file(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def get_tests_path(pipeline_type):
    json_path = f"tests/tests_{pipeline_type}.json"
    feature_path = f"tests/tests_{pipeline_type}.feature"
    if os.path.exists(json_path):
        return json_path
    return feature_path


def count_jsonl_lines(filepath):
    if not os.path.exists(filepath):
        return 0
    total = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                total += 1
    return total


def normalize_root_list(data, primary_key):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if primary_key in data and isinstance(data[primary_key], list):
            return data[primary_key]
        for value in data.values():
            if isinstance(value, list):
                return value
    return []


def extract_review_groups(groups_data):
    groups = normalize_root_list(groups_data, "groups")
    normalized = []

    for idx, group in enumerate(groups):
        if not isinstance(group, dict):
            continue

        group_id = (
            group.get("group_id")
            or group.get("id")
            or group.get("review_group_id")
            or group.get("theme_id")
            or f"group_{idx + 1}"
        )

        review_ids = group.get("review_ids", [])
        if not isinstance(review_ids, list):
            review_ids = []

        normalized.append({
            "group_id": str(group_id),
            "review_ids": [str(rid) for rid in review_ids]
        })

    return normalized


def extract_personas(personas_data):
    personas = normalize_root_list(personas_data, "personas")
    normalized = []

    for idx, persona in enumerate(personas):
        if not isinstance(persona, dict):
            continue

        # MODIFIED: Prioritize the 'name' field first so it matches the Markdown specs exactly.
        persona_id = (
            persona.get("name")
            or persona.get("persona_id")
            or persona.get("id")
            or f"persona_{idx + 1}"
        )

        review_group_ref = (
            persona.get("review_group_id")
            or persona.get("review_group")
            or persona.get("source_group")
            or persona.get("group_id")
            or persona.get("derived_from_group")
            or persona.get("origin_group")
        )

        normalized.append({
            "persona_id": str(persona_id),
            "review_group_ref": "" if review_group_ref is None else str(review_group_ref)
        })

    return normalized


def detect_label(line):
    stripped = line.strip()
    for field_name, labels in RECOGNIZED_FIELDS.items():
        for label in labels:
            pattern = rf"^(?:[#>\-\*\s]*){re.escape(label)}\s*:\s*(.*)$"
            match = re.match(pattern, stripped, flags=re.IGNORECASE)
            if match:
                return field_name, match.group(1).strip()
    return None, None


def split_requirement_blocks(markdown_text):
    pattern = re.compile(r"(?im)^(?:[#>\-\*\s]*)Requirement ID\s*:")
    matches = list(pattern.finditer(markdown_text))

    if not matches:
        return []

    blocks = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown_text)
        blocks.append(markdown_text[start:end].strip())

    return blocks


def parse_requirement_block(block_text):
    fields = defaultdict(list)
    current_field = None

    for raw_line in block_text.splitlines():
        line = raw_line.rstrip()

        if not line.strip():
            continue

        field_name, value = detect_label(line)
        if field_name:
            current_field = field_name
            if value:
                fields[field_name].append(value)
            continue

        if current_field:
            cleaned = line.strip()
            cleaned = re.sub(r"^[\-\*\d\.\)\s]+", "", cleaned).strip()
            if cleaned:
                fields[current_field].append(cleaned)

    return {
        "requirement_id": " ".join(fields["req_id"]).strip(),
        "description": " ".join(fields["description"]).strip(),
        "persona_ref": " ".join(fields["persona"]).strip(),
        "review_group_ref": " ".join(fields["review_group"]).strip(),
        "acceptance_criteria": " ".join(fields["acceptance"]).strip(),
        "raw_block": block_text.strip()
    }


def extract_requirements(spec_path):
    if not os.path.exists(spec_path):
        return []

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = split_requirement_blocks(content)
    requirements = []

    for block in blocks:
        parsed = parse_requirement_block(block)
        if parsed["requirement_id"]:
            requirements.append(parsed)

    return requirements


def extract_requirement_reference_from_test(test_obj):
    if not isinstance(test_obj, dict):
        return ""

    for key in [
        "requirement_id",
        "requirement",
        "req_id",
        "validates_requirement",
        "linked_requirement",
        "requirement_ref"
    ]:
        value = test_obj.get(key)
        if value:
            return str(value).strip()

    return ""


def extract_tests_from_json(tests_path):
    data = load_json_file(tests_path)
    tests = normalize_root_list(data, "tests")
    normalized = []

    for idx, test in enumerate(tests):
        if not isinstance(test, dict):
            continue

        test_id = test.get("test_id") or test.get("id") or f"test_{idx + 1}"
        req_ref = extract_requirement_reference_from_test(test)

        normalized.append({
            "test_id": str(test_id),
            "requirement_ref": req_ref
        })

    return normalized


def extract_tests_from_feature(tests_path):
    if not os.path.exists(tests_path):
        return []

    tests = []
    current_tags = []
    scenario_count = 0

    with open(tests_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()

            if not line:
                continue

            if line.startswith("@"):
                current_tags = line.split()
                continue

            if line.lower().startswith("scenario:") or line.lower().startswith("scenario outline:"):
                scenario_count += 1
                req_ref = ""

                for tag in current_tags:
                    match = re.search(r"(REQ[_-]?\d+|FR[_-]?\d+)", tag, flags=re.IGNORECASE)
                    if match:
                        req_ref = match.group(1)
                        break

                if not req_ref:
                    match = re.search(r"(REQ[_-]?\d+|FR[_-]?\d+)", line, flags=re.IGNORECASE)
                    if match:
                        req_ref = match.group(1)

                tests.append({
                    "test_id": f"scenario_{scenario_count}",
                    "requirement_ref": req_ref
                })

                current_tags = []

    return tests


def extract_tests(tests_path):
    if tests_path.endswith(".feature"):
        return extract_tests_from_feature(tests_path)
    return extract_tests_from_json(tests_path)


def normalize_requirement_id(value):
    if not value:
        return ""

    value = str(value).strip()
    match = re.search(r"(REQ[_-]?\d+|FR[_-]?\d+)", value, flags=re.IGNORECASE)

    if match:
        return match.group(1).upper().replace("_", "-")

    return value.upper().replace("_", "-")


def normalize_persona_ref(value):
    if not value:
        return ""

    value = str(value).strip()
    # If the user put a full name, this regex bypasses it and lowercases the whole string.
    match = re.search(r"(persona[_-]?\d+|P[_-]?\d+)", value, flags=re.IGNORECASE)

    if match:
        return match.group(1).lower().replace("-", "_")

    return value.lower()


def contains_ambiguous_language(text):
    if not text:
        return False

    lowered = text.lower()
    for term in AMBIGUOUS_TERMS:
        if re.search(rf"\b{re.escape(term.lower())}\b", lowered):
            return True

    return False


def calculate_metrics(pipeline_type="auto"):
    print(f"Calculating metrics for the '{pipeline_type}' pipeline...")

    clean_data_path = "data/reviews_clean.jsonl"
    groups_path = f"data/review_groups_{pipeline_type}.json"
    personas_path = f"personas/personas_{pipeline_type}.json"
    spec_path = f"spec/spec_{pipeline_type}.md"
    tests_path = get_tests_path(pipeline_type)

    total_reviews = count_jsonl_lines(clean_data_path)

    review_groups = extract_review_groups(load_json_file(groups_path))
    personas = extract_personas(load_json_file(personas_path))
    requirements = extract_requirements(spec_path)
    tests = extract_tests(tests_path)

    persona_count = len(personas)
    req_count = len(requirements)
    test_count = len(tests)

    unique_review_ids = set()
    for group in review_groups:
        unique_review_ids.update(group["review_ids"])

    review_coverage = round((len(unique_review_ids) / total_reviews), 4) if total_reviews > 0 else 0.0

    valid_group_refs = {str(group["group_id"]).strip().lower() for group in review_groups}
    persona_to_group_links = 0
    for persona in personas:
        ref = str(persona["review_group_ref"]).strip().lower()
        if ref and ref in valid_group_refs:
            persona_to_group_links += 1

    normalized_persona_ids = {normalize_persona_ref(p["persona_id"]) for p in personas}
    requirement_to_persona_links = 0
    requirements_with_persona = 0
    for requirement in requirements:
        persona_ref = normalize_persona_ref(requirement["persona_ref"])
        if persona_ref and persona_ref in normalized_persona_ids:
            requirements_with_persona += 1
            requirement_to_persona_links += 1

    valid_requirement_ids = {normalize_requirement_id(req["requirement_id"]) for req in requirements}
    test_to_requirement_links = 0
    linked_requirement_ids = set()
    for test in tests:
        req_ref = normalize_requirement_id(test["requirement_ref"])
        if req_ref and req_ref in valid_requirement_ids:
            test_to_requirement_links += 1
            linked_requirement_ids.add(req_ref)

    traceability_links = persona_to_group_links + requirement_to_persona_links + test_to_requirement_links
    traceability_ratio = round((requirements_with_persona / req_count), 4) if req_count > 0 else 0.0

    testable_requirements = 0
    for req in requirements:
        req_id = normalize_requirement_id(req["requirement_id"])
        if req_id in linked_requirement_ids:
            testable_requirements += 1

    testability_rate = round((testable_requirements / req_count), 4) if req_count > 0 else 0.0

    ambiguous_requirements = 0
    for req in requirements:
        text_to_check = f"{req['description']} {req['acceptance_criteria']}".strip()
        if contains_ambiguous_language(text_to_check):
            ambiguous_requirements += 1

    ambiguity_ratio = round((ambiguous_requirements / req_count), 4) if req_count > 0 else 0.0

    output = {
        "pipeline": pipeline_type,
        "dataset_size": total_reviews,
        "persona_count": persona_count,
        "requirements_count": req_count,
        "tests_count": test_count,
        "traceability_links": traceability_links,
        "review_coverage": review_coverage,
        "traceability_ratio": traceability_ratio,
        "testability_rate": testability_rate,
        "ambiguity_ratio": ambiguity_ratio
    }

    os.makedirs("metrics", exist_ok=True)
    out_file = f"metrics/metrics_{pipeline_type}.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Success: {out_file} saved.")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    target = sys.argv[1].strip().lower() if len(sys.argv) > 1 else "auto"
    calculate_metrics(target)