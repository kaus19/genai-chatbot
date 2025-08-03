import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="fact Generator",
    page_icon="📚",
    layout="centered"
)

# Add title
st.title("✨ AI fact Generator")

# Add a section to view documents
st.markdown("## 📑 View Stored Documents")
if st.button("Show All Documents"):
    try:
        response = requests.get("http://localhost:8000/documents")
        if response.status_code == 200:
            data = response.json()
            st.write("### Collection Statistics")
            st.json(data["collection_stats"])
            
            st.write("### Stored Documents")
            for doc in data["documents"]:
                st.markdown("---")
                st.write(f"**ID:** {doc['id']}")
                st.write(f"**Content:** {doc['text']}")
                st.write(f"**Metadata:** {doc['metadata']}")
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the server")

# Add a new section for document upload
st.markdown("## 📚 Upload Knowledge")
doc_content = st.text_area("Enter document content:", height=150)
doc_metadata = st.text_input("Enter metadata (optional, as JSON):", "{}")

if st.button("Upload Document"):
    try:
        metadata = json.loads(doc_metadata)
        response = requests.post(
            "http://localhost:8000/upload-document",
            json={"content": doc_content, "metadata": metadata}
        )
        if response.status_code == 200:
            st.success("Document uploaded successfully!")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        st.error("Invalid JSON in metadata field")
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the server")

# Create input field for fact prompt
prompt = st.text_area("Enter your fact prompt:", height=100)

# Create generate button
if st.button("Generate Fact"):
    if prompt:
        try:
            # Call the FastAPI endpoint
            response = requests.post(
                "http://localhost:8000/generate-fact",
                json={"prompt": prompt}
            )
            
            if response.status_code == 200:
                # Display the generated fact
                fact = response.json()["fact"]
                st.success("fact generated successfully!")
                st.markdown("### Your fact:")
                st.write(fact)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the server. Make sure the FastAPI backend is running.")
    else:
        st.warning("Please enter a prompt first!")

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and FastAPI")