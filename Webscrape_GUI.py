import Webscrape
import streamlit as st
from docx import Document

st.write("""   
# In-text Citation Generator

Insert your document with PubMed links to convert them to in-text citations

""")

with st.form(key = "form1"):
    document = st.text_area("Insert document text", height = 400)
    delimiter = st.text_input("Insert delimiter", help = "Set the border you wish to surround your PubMed links, by default it will be []" ,placeholder = "[]")
    if st.form_submit_button("Process document", help = "After entering your document, you can press this button to create a cited file"):
        if delimiter == '':
            delimiter = "[]"
        cited_document = Webscrape.document_citation(document, delimiter)
        #st.write(cited_document)



with st.form(key = "form2"):
    uploaded_file = st.file_uploader("Upload document or text file", type=['.txt', '.docx'])
    delimiter = st.text_input("Insert delimiter", help = "Set the border you wish to surround your PubMed links, by default it will be []" ,placeholder = "[]")
    if st.form_submit_button("Process file", help = "Process the file you uploaded") and uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            #st.text(str(uploaded_file.read(),"utf-8"))
            document = str(uploaded_file.read(),"utf-8")
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            document = Document(uploaded_file)
            document = ''.join([str(paragraph.text) for paragraph in document.paragraphs])
        if delimiter == '':
            delimiter = "[]"
        cited_document = Webscrape.document_citation(document, delimiter)
        #st.write(cited_document)


try:
    st.write(cited_document)
    file_name = st.text_input("File name", help = "Set your file_name")
    st.download_button (label = "Download Cited Document", data = cited_document, file_name = file_name)
except:
    pass