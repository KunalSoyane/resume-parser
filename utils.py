import pdfplumber
import re
import spacy
from spacy.matcher import PhraseMatcher

# Load the model once here so we can use it in functions
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    """Extracts raw text from a PDF file."""
    full_text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

def extract_contact_info(text):
    """Extracts email and phone using Regex."""
    contact_info = {"email": None, "phone": None}
    
    # Email Pattern
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact_info["email"] = email_match.group()

    # Phone Pattern
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        contact_info["phone"] = phone_match.group()

    return contact_info

def extract_skills(text, skills_list):
    """Extracts skills using spaCy PhraseMatcher."""
    doc = nlp(text)
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(skill) for skill in skills_list]
    matcher.add("SKILLS", patterns)
    
    matches = matcher(doc)
    found_skills = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        found_skills.add(span.text)
    return list(found_skills)

def extract_name(text):
    """
    Extracts name with multiple strategies:
    1. First Line (if isolated).
    2. First 2 words of First Line (if merged and uppercase).
    3. SpaCy NER (as fallback, with filters).
    """
    # Clean text and split into lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    if lines:
        first_line = lines[0]
        words = first_line.split()
        
        # Strategy 1: Isolated Name (e.g., "John Doe")
        # If the first line is 2-3 words and mostly letters
        if 2 <= len(words) <= 3 and all(w.isalpha() for w in words):
            return first_line.title()
            
        # Strategy 2: Merged Line (e.g., "JOHN DOE Software Engineer")
        # If the first 2 words are ALL CAPS, they are likely the name.
        if len(words) > 3 and words[0].isupper() and words[1].isupper():
            return f"{words[0]} {words[1]}".title()

    # Strategy 3: SpaCy Fallback (AI)
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # FILTER: Ignore common mistakes (Job Titles)
            lower_text = ent.text.lower()
            if "enthusiast" in lower_text or "engineer" in lower_text or "developer" in lower_text:
                continue
            return ent.text
            
    return "Unknown"
