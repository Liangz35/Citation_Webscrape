import streamlit as st
import Webscrape


st.write("""   
# In-text Citation Generator

Insert your document with PubMed links to convert them to in-text citations

""")

with st.form(key = "form1"):
    document = st.text_area("Insert document text", height = 600)
    delimiter = st.text_input("Insert delimiter")
    if st.form_submit_button("Read document", help = "After entering your document, you can press this button to create a cited file"):
        st.write(Webscrape.document_citation(document, delimiter))



uploaded_file = st.file_uploader("Upload document or text file", type = ['.txt','.docx'])
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    st.write(string_data)
