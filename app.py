import streamlit as st
import PyPDF2

st.set_page_config(page_title="Resume Job Matcher", page_icon="📄")

job_roles = {
    "Data Scientist": ["python", "machine learning", "pandas", "numpy", "statistics"],
    "Frontend Developer": ["html", "css", "javascript", "react"],
    "Backend Developer": ["java", "spring", "sql", "api", "rest"],
    "AI Engineer": ["deep learning", "pytorch", "tensorflow", "neural networks"],
    "Business Analyst": ["excel", "data analysis", "reporting", "sql", "power bi"]
}

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

def suggest_jobs(text):
    suggestions = []
    for role, keywords in job_roles.items():
        matches = sum(1 for kw in keywords if kw in text)
        if matches >= 2:
            suggestions.append((role, matches))
    return sorted(suggestions, key=lambda x: x[1], reverse=True)

st.title("📄 Resume-Based Job Suggestion Bot")
st.write("Upload your resume and get job role suggestions based on your skills!")

uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type="pdf")

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.success("✅ Resume processed successfully.")

    st.subheader("💼 Suggested Job Roles:")
    suggestions = suggest_jobs(text)
    if suggestions:
        for role, score in suggestions:
            st.info(f"{role} — {score} skill match")
    else:
        st.warning("No matching job role found.")

    with st.expander("📄 Show Extracted Resume Text"):
        st.text(text)

import openai

openai.api_key = st.secrets.get("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")  # secure way

st.subheader("🤖 Ask the Resume Advisor")

user_query = st.chat_input("Ask about your resume or job fit...")

if user_query and uploaded_file:
    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful resume advisor. The resume content is:\n{text}"},
                {"role": "user", "content": user_query}
            ]
        )
        st.write(response['choices'][0]['message']['content'])
