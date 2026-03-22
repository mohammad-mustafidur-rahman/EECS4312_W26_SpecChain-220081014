import os
import json
import httpx
from groq import Groq

def run_test_automation():
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        http_client=httpx.Client(verify=False)
    )

    try:
        with open('spec/spec_auto.md', 'r', encoding='utf-8') as f:
            spec_content = f.read()
    except FileNotFoundError:
        print("Error: spec/spec_auto.md not found.")
        return

    prompt = f"""
    Read this software specification: 
    {spec_content}
    
    Generate a validation test suite in JSON format. Every requirement listed in the spec MUST have at least one test scenario.
    
    You MUST output ONLY a valid JSON object matching this exact structure:
    {{
      "tests": [
        {{
          "test_id": "T_auto_1",
          "requirement_id": "FR_auto_1",
          "scenario": "Logging a workout without crashing",
          "steps": [
            "Open the workout logging screen",
            "Enter workout details"
          ],
          "expected_result": "The workout is saved successfully."
        }}
      ]
    }}
    """

    print("Asking Groq to generate validation tests...")
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    os.makedirs('tests', exist_ok=True)
    with open('tests/tests_auto.json', 'w', encoding='utf-8') as f:
        f.write(response.choices[0].message.content)
        
    print("Success: tests/tests_auto.json created.")

if __name__ == "__main__":
    run_test_automation()