import streamlit as st
import fitz  # PyMuPDF
import docx
import spacy
import re

nlp = spacy.load("en_core_web_sm")

st.title("📄 Resume Analyzer")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

def extract_text_from_pdf(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_info(text):
    doc = nlp(text)
    name = ""
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break
    email = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
", text)
    phone = re.findall(r"\+?\d{1,4}?[-.\s]?\(?\d{2,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{4}"
, text)
    return {
        "Name": name,
        "Email": email[0] if email else "Not found",
        "Phone": phone[0] if phone else "Not found"
    }

if uploaded_file:
    st.success("Resume uploaded!")

    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_docx(uploaded_file)

    info = extract_info(text)

    st.subheader("📌 Extracted Information:")
    st.write(info)

    st.subheader("🧾 Resume Text:")
    st.text_area("Parsed Text", text, height=300)
