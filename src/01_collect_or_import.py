import json
import os
from google_play_scraper import Sort, reviews

def fetch_minddoc_reviews():
    app_id = 'de.moodpath.android'
    target_review_count = 3000 
    
    print(f"Fetching {target_review_count} reviews for {app_id}...")
    
    try:
        result, continuation_token = reviews(
            app_id,
            lang='en', 
            country='ca', # Using the Canadian store based on your URL
            sort=Sort.NEWEST, 
            count=target_review_count 
        )
        
        print(f"Successfully fetched {len(result)} reviews.")
        
        os.makedirs('data', exist_ok=True)
        output_file = 'data/reviews_raw.jsonl'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for review in result:
                # Convert datetime to string for JSON serialization
                if review.get('at'):
                    review['at'] = review['at'].strftime('%Y-%m-%d %H:%M:%S')
                if review.get('repliedAt'):
                    review['repliedAt'] = review['repliedAt'].strftime('%Y-%m-%d %H:%M:%S')
                
                f.write(json.dumps(review) + '\n')
                
        print(f"Saved raw reviews to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_minddoc_reviews()
