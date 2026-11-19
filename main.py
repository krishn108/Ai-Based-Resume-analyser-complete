
import streamlit as st

st.set_page_config(
    page_title="PDF Upload Test",
    page_icon="📄"
)

st.title("PDF Upload Testing")

st.write("Select your PDF file below.")

uploaded_file = st.file_uploader(
    "Choose PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("PDF Uploaded Successfully!")

    st.write("File Name:", uploaded_file.name)

    st.write("File Size:", uploaded_file.size)

    file_data = uploaded_file.getvalue()

    st.write("Received Bytes:", len(file_data))

    if file_data:

        st.success("File received by Python successfully.")

        st.download_button(
            "Download Uploaded PDF",
            data=file_data,
            file_name=uploaded_file.name,
            mime="application/pdf"
        )

    else:

        st.error("Empty file received.")
        
