import re
import string

def clean_text(text: str) -> str:
    """
    Cleans the input text by:
    1. Converting to lowercase.
    2. Removing special characters and punctuation.
    3. Removing extra whitespace.
    """
    if not isinstance(text, str):
        return ""
    
    # optimize: remove HTML tags first if any (simple regex)
    text = re.sub(r'<[^>]+>', '', text)
    
    # Lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers (optional, but good for generic text classification)
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    return text
