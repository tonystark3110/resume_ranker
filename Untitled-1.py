import os
import PyPDF2
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to preprocess text
def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text.lower())
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Join tokens back into text
    preprocessed_text = ' '.join(filtered_tokens)
    return preprocessed_text

# Directory containing resumes in PDF format
pdf_folder_path = 'C:/Users/Manikandan/Desktop/z'

# Keywords for ranking
keywords = ['machine learning', 'data analyst', 'programming skills', 'project manager', 'communication skills']

# List to store ranked resumes
ranked_resumes = []

# Process resumes and calculate relevance scores based on keywords
for filename in os.listdir(pdf_folder_path):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder_path, filename)
        resume_text = extract_text_from_pdf(pdf_path)
        preprocessed_resume = preprocess_text(resume_text)

        # Calculate relevance score based on presence of keywords
        relevance_score = sum(preprocessed_resume.count(keyword) for keyword in keywords)

        ranked_resumes.append((filename, relevance_score))

# Select the resume with the highest relevance score
top_resume = max(ranked_resumes, key=lambda x: x[1])[0]

# Extract email address from the top-ranked resume
email_pattern = r'[\w\.-]+@[\w\.-]+'
resume_text = extract_text_from_pdf(os.path.join(pdf_folder_path, top_resume))
email_match = re.search(email_pattern, resume_text)
if email_match:
    email_address = email_match.group(0)
    print("Email address extracted from the top-ranked resume:", email_address)
else:
    print("No email address found in the top-ranked resume.")

# Send email notification to the extracted email address using SendGrid SMTP server
smtp_server = 'smtp.sendgrid.net'
smtp_port = 587  # TLS port
sender_email = 'mani'
sender_password = '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'
recipient_email = email_address

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = 'Interview Invitation'
body = f'Congratulations! You have been selected for an interview. Please reply to this email to confirm your availability.'
msg.attach(MIMEText(body, 'plain'))

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())

print("Email sent successfully to:", recipient_email)





