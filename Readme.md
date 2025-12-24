# 📄 AI Resume Parser

A Natural Language Processing (NLP) tool that extracts meaningful information from PDF resumes using Python.

**[🔴 Live Demo](https://resume-parser-qy5vdto7j7zpirwtoqrrwe.streamlit.app/)**

## 🚀 Features
- **Information Extraction**: Automatically pulls Name, Email, and Phone Number using RegEx.
- **Skill Matching**: Uses `spaCy` (NLP) to identify technical skills (Python, SQL, Machine Learning) from a predefined knowledge base.
- **PDF Processing**: handles complex layouts using `pdfplumber`.

## 🛠️ Tech Stack
- **Python 3.10**
- **Streamlit** (Frontend)
- **spaCy** (NLP Model: `en_core_web_sm`)
- **pdfplumber** (PDF Extraction)

## 📦 How to Run Locally

1. **Clone the repo**
   ```bash
   git clone [https://github.com/KunalSoyane/resume-parser.git](https://github.com/KunalSoyane/resume-parser.git)
   cd resume-parser
