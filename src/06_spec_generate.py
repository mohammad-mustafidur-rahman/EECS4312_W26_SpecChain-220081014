import os
import json
import httpx
from groq import Groq

def run_spec_automation():
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        http_client=httpx.Client(verify=False)
    )

    try:
        with open('personas/personas_auto.json', 'r', encoding='utf-8') as f:
            personas = json.load(f)
    except FileNotFoundError:
        print("Error: personas/personas_auto.json not found.")
        return

    prompt = f"""
    Based on these user personas: {json.dumps(personas)}, generate a software specification in Markdown.
    
    You MUST write exactly 10 requirements. 
    For each requirement, use the EXACT format below, including the brackets. Separate requirements with a blank line. Do not use Markdown headings like ###.

    ### Requirement ID: FR_auto_1
    - Description: [Clear description of system behavior]
    - Source Persona: [Persona Name]
    - Traceability: [Derived from review group A1]
    - Acceptance Criteria:[Given... When... Then...]
    """

    print("Asking Groq to generate software specifications...")
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.2
    )

    os.makedirs('spec', exist_ok=True)
    with open('spec/spec_auto.md', 'w', encoding='utf-8') as f:
        f.write(response.choices[0].message.content)
        
    print("Success: spec/spec_auto.md created.")

if __name__ == "__main__":
    run_spec_automation()