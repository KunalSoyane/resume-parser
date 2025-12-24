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
    Tries to find a person's name using spaCy NER.
    Fallback: Returns the first line of the text if no name found.
    """
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Unknown"
