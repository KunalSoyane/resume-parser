from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

def create_resume():
    c = canvas.Canvas("sample_resume.pdf", pagesize=LETTER)
    
    # 1. Name & Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, 750, "JOHN DOE")
    c.setFont("Helvetica", 12)
    c.drawString(50, 735, "Software Engineer | Data Enthusiast")
    
    # 2. Contact Info (This is what your Regex looks for!)
    c.setFont("Helvetica", 10)
    c.drawString(50, 715, "Email: johndoe123@email.com")
    c.drawString(50, 700, "Phone: (555) 123-4567")
    c.drawString(50, 685, "Location: New York, NY")
    
    c.line(50, 675, 550, 675) # Horizontal line
    
    # 3. Skills Section (This is what spaCy looks for!)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 650, "SKILLS")
    c.setFont("Helvetica", 10)
    # Note: These match the keywords in your SKILLS_DB list
    c.drawString(50, 630, "• Programming: Python, Java, C++, SQL")
    c.drawString(50, 615, "• Frameworks: React, React.js, Flask")
    c.drawString(50, 600, "• Cloud & Tools: AWS, Docker, Git, Linux")
    c.drawString(50, 585, "• Soft Skills: Leadership, Communication")

    # 4. Experience Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 550, "EXPERIENCE")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 530, "Tech Solutions Inc. - Junior Developer")
    c.setFont("Helvetica", 10)
    c.drawString(50, 515, "Jan 2022 - Present")
    c.drawString(65, 500, "- Built REST APIs using Python and Flask.")
    c.drawString(65, 485, "- managed databases with SQL and optimized queries.")
    c.drawString(65, 470, "- Deployed applications using Docker and AWS.")

    # 5. Education
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 440, "EDUCATION")
    c.setFont("Helvetica", 10)
    c.drawString(50, 420, "B.Tech in Computer Science")
    c.drawString(50, 405, "University of Technology, 2021")

    c.save()
    print("✅ Success! 'sample_resume.pdf' has been created.")

if __name__ == "__main__":
    create_resume()
