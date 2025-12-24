import streamlit as st
import pdfplumber
import re
import spacy
from spacy.matcher import PhraseMatcher

# --- 1. SETUP & CONFIG ---
# st.set_page_config makes the tab title look good
st.set_page_config(page_title="AI Resume Parser", page_icon="📄")

# Load NLP model efficiently (cache it so it doesn't reload on every click)
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")

nlp = load_model()

# Our Knowledge Base
SKILLS_DB = [
    "Python", "Java", "C++", "SQL", "Machine Learning",
    "Data Science", "React", "React.js", "AWS", "Azure",
    "Docker", "Kubernetes", "HTML", "CSS", "JavaScript",
    "Communication", "Leadership", "Git", "Linux"
]

# --- 2. CORE FUNCTIONS (Same as before) ---

def extract_text_from_pdf(file):
    """
    Modified to handle Streamlit's file uploader object directly
    """
    full_text = ""
    # pdfplumber can open file-like objects (streams) directly!
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

def extract_contact_info(text):
    contact_info = {"email": None, "phone": None}
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
    
    email_match = re.search(email_pattern, text)
    if email_match:
        contact_info["email"] = email_match.group()
        
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        contact_info["phone"] = phone_match.group()
        
    return contact_info

def extract_skills(text, skills_list):
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

import pandas as pd
        if skills:
                st.subheader("📊 Skills Visualization")
                df = pd.DataFrame(skills, columns=["Skill"])
                st.bar_chart(df)

# --- 3. THE STREAMLIT UI ---

def main():
    st.title("📄 AI Resume Parser")
    st.write("Upload a resume (PDF) to extract contact info and skills.")

    st.write("Don't have a resume? Download this sample to test it:")
    with open("sample_resume.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Download Sample Resume",
                        data=PDFbyte,
                        file_name="sample_resume.pdf",
                        mime='application/octet-stream')

    # File Uploader Widget
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        try:
            with st.spinner('Reading Resume...'):
                # 1. Extract Text
                resume_text = extract_text_from_pdf(uploaded_file)
                
                # 2. Extract Info
                contact = extract_contact_info(resume_text)
                skills = extract_skills(resume_text, SKILLS_DB)

            # 3. Display Results
            st.success("Resume processed successfully!")
            
            # Create two columns for layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📞 Contact Info")
                st.text_input("Email", value=contact['email'] if contact['email'] else "Not Found")
                st.text_input("Phone", value=contact['phone'] if contact['phone'] else "Not Found")

            with col2:
                st.subheader("🛠 Skills Found")
                st.write(f"Found {len(skills)} skills:")
                # Display skills as colorful "chips"
                st.pills("Skills", skills, selection_mode="multi")

            # Show Raw Text (Optional, inside an expander)
            with st.expander("See Raw Extracted Text"):
                st.text(resume_text)

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":

    main()


