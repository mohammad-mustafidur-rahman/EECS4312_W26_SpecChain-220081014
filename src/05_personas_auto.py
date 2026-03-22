import os
import json
import httpx
from groq import Groq

def run_persona_automation():
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        http_client=httpx.Client(verify=False)
    )

    reviews_data = []
    try:
        with open('data/reviews_clean.jsonl', 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= 100: break
                review = json.loads(line)
                r_id = review.get('reviewId') or review.get('id') or f"rev_{i}"
                reviews_data.append({"id": r_id, "content": review.get('content', '')})
    except FileNotFoundError:
        print("Error: data/reviews_clean.jsonl not found.")
        return

    prompt = f"""
    You are a requirements engineer analyzing these MindDoc app reviews: {reviews_data}.
    1. Group them into exactly 5 distinct themes.
    2. Create exactly 5 user personas, one for each theme.
    
    You MUST output ONLY a valid JSON object with exactly two top-level keys: "groups" and "personas".
    
    The "groups" array MUST follow this exact structure:
    [
      {{
        "group_id": "A1",
        "theme": "Theme description",
        "review_ids": ["id1", "id2"],
        "example_reviews": ["Review text 1", "Review text 2"]
      }}
    ]
    
    The "personas" array MUST contain objects with "id", "name", "description", "derived_from_group" (matching the group_id), "goals" (list), and "pain_points" (list).
    """
    
    os.makedirs('prompts', exist_ok=True)
    with open('prompts/prompt_auto.json', 'w', encoding='utf-8') as f:
        json.dump({"prompt": prompt}, f, indent=2)

    print("Asking Groq to generate review groups and personas...")
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    
    os.makedirs('data', exist_ok=True)
    os.makedirs('personas', exist_ok=True)
    
    with open('data/review_groups_auto.json', 'w', encoding='utf-8') as f:
        json.dump({"groups": result.get("groups", [])}, f, indent=2)
        
    with open('personas/personas_auto.json', 'w', encoding='utf-8') as f:
        json.dump({"personas": result.get("personas", [])}, f, indent=2)
        
    print("Success: review_groups_auto.json, personas_auto.json, and prompt_auto.json created.")

if __name__ == "__main__":
    run_persona_automation()