import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Energy Market RAG Assistant",
    layout="wide"
)

st.title("Energy Market Intelligence RAG Assistant")

st.write(
    "Upload electricity market reports, PDFs, CSVs, or notes and ask natural language questions."
)

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "csv", "txt"]
)

if uploaded_file:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    response = requests.post(f"{API_URL}/upload", files=files)

    if response.status_code == 200:
        st.success("File uploaded and indexed successfully.")
        st.json(response.json())
    else:
        st.error("Upload failed.")

st.divider()

question = st.text_input(
    "Ask a question about the uploaded energy market documents"
)

if st.button("Ask"):
    if not question:
        st.warning("Please enter a question.")
    else:
        response = requests.post(
            f"{API_URL}/ask",
            json={"question": question}
        )

        if response.status_code == 200:
            result = response.json()

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Sources")
            st.json(result["sources"])

            with st.expander("Retrieved Context"):
                for chunk in result["retrieved_context"]:
                    st.write(chunk)
                    st.divider()
        else:
            st.error("Question answering failed.")