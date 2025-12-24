import streamlit as st
import pandas as pd
# Import the logic from our new utils.py file
from utils import extract_text_from_pdf, extract_contact_info, extract_skills, extract_name

# --- CONFIG ---
st.set_page_config(page_title="AI Resume Parser", page_icon="📄")

# Our Knowledge Base
SKILLS_DB = [
    "Python", "Java", "C++", "SQL", "Machine Learning",
    "Data Science", "React", "React.js", "AWS", "Azure",
    "Docker", "Kubernetes", "HTML", "CSS", "JavaScript",
    "Communication", "Leadership", "Git", "Linux"
]

# --- MAIN APP ---
def main():
    st.title("📄 AI Resume Parser")
    st.write("Upload a resume (PDF) to extract contact info, skills, and generate a report.")

    # --- DOWNLOAD SAMPLE ---
    try:
        with open("sample_resume.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()
        st.download_button(label="Download Sample Resume",
                            data=PDFbyte,
                            file_name="sample_resume.pdf",
                            mime='application/octet-stream')
    except FileNotFoundError:
        st.warning("Note: 'sample_resume.pdf' not found. Upload your own.")

    # --- UPLOAD SECTION ---
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        try:
            with st.spinner('Reading Resume...'):
                # 1. Call functions from utils.py
                resume_text = extract_text_from_pdf(uploaded_file)
                contact = extract_contact_info(resume_text)
                skills = extract_skills(resume_text, SKILLS_DB)
                name = extract_name(resume_text)

            st.success("Resume processed successfully!")
            
            # 2. Display Results
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("👤 Candidate Info")
                st.text_input("Name", value=name)
                st.text_input("Email", value=contact['email'] if contact['email'] else "Not Found")
                st.text_input("Phone", value=contact['phone'] if contact['phone'] else "Not Found")

            with col2:
                st.subheader("🛠 Skills Found")
                st.write(f"Found {len(skills)} skills:")
                st.pills("Skills", skills, selection_mode="multi")

            # 3. Visualization
            if skills:
                st.subheader("📊 Skills Visualization")
                df = pd.DataFrame({"Skill": skills, "Count": [1]*len(skills)})
                st.bar_chart(df.set_index("Skill"))

            # 4. CSV Export (The new feature!)
            st.divider()
            st.subheader("💾 Export Report")
            
            # Prepare data for CSV
            report_data = {
                "Name": [name],
                "Email": [contact['email']],
                "Phone": [contact['phone']],
                "Skills": [", ".join(skills)]
            }
            df_report = pd.DataFrame(report_data)
            csv = df_report.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Download Resume Data (CSV)",
                data=csv,
                file_name='resume_parsed.csv',
                mime='text/csv',
            )

            # Raw text expander
            with st.expander("See Raw Extracted Text"):
                st.text(resume_text)

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
