import json
import re
import string
import inflect
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import ssl

# This bypasses the SSL certificate verification error on macOS
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data on first run
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

p = inflect.engine()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def convert_numbers_to_text(text):
    words = text.split()
    new_words = []
    for word in words:
        if word.isdigit():
            new_words.append(p.number_to_words(word))
        else:
            new_words.append(word)
    return " ".join(new_words)

def clean_review(text):
    # Remove empty or extremely short reviews (less than 3 words)
    if not text or len(text.split()) < 3: 
        return None
    
    # Remove emojis and special characters by encoding to ASCII
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Convert numbers to text
    text = convert_numbers_to_text(text)
    
    # Convert to lowercase and remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip().lower()
    
    # Remove stop words and lemmatize
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    
    # Re-check length after cleaning
    if len(words) < 3:
        return None
        
    return " ".join(words)

def main():
    cleaned_reviews = []
    seen_reviews = set()

    with open('data/reviews_raw.jsonl', 'r', encoding='utf-8') as infile:
        for line in infile:
            data = json.loads(line)
            raw_text = data.get('content', '') 
            
            clean_text = clean_review(raw_text)
            
            # Keep only unique reviews
            if clean_text and clean_text not in seen_reviews:
                seen_reviews.add(clean_text)
                data['content'] = clean_text # Replace content with cleaned version
                cleaned_reviews.append(data)

    with open('data/reviews_clean.jsonl', 'w', encoding='utf-8') as outfile:
        for review in cleaned_reviews:
            outfile.write(json.dumps(review) + '\n')
            
    print(f"Cleaning complete. Retained {len(cleaned_reviews)} valid, unique reviews.")

if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 81cdb4d (Saving local work before syncing with GitHub)
