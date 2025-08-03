import streamlit as st
import requests
import json
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="AI Chat & Fact Generator",
    page_icon="📚",
    layout="centered"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add title
st.title("✨ AI Chat & Fact Generator")

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📚 Documents", "🎯 Fact Generator"])

with tab1:
    st.markdown("### 💬 Chat with AI")
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input using standard text input
    prompt = st.text_input("Your message:", key="chat_input")
    
    if st.button("Send", key="send_button"):
        if prompt:  # Check if input is not empty
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            try:
                # Show loading indicator
                with st.spinner("AI is thinking..."):
                    # Send request to backend
                    response = requests.post(
                        "http://localhost:8000/chat",
                        json={"content": prompt, "role": "user"},
                        timeout=30  # Add timeout
                    )
                
                if response.status_code == 200:
                    response_data = response.json()
                    assistant_response = response_data["response"]
                    
                    # Display assistant response
                    with st.chat_message("assistant"):
                        st.markdown(assistant_response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_response}
                    )
                    
                    # Clear input after successful response
                    # st.session_state.chat_input = ""
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the server. Please check if the backend is running.")
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
        else:
            st.warning("Please enter a message first!")

with tab2:
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
                st.error(f"Error: {response.status_code}")
        except json.JSONDecodeError:
            st.error("Invalid JSON in metadata field")
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the server")

with tab3:
    st.markdown("## 🎯 Generate Facts")
    fact_prompt = st.text_area("Enter your prompt:", height=100)
    
    if st.button("Generate Fact"):
        if fact_prompt:
            try:
                response = requests.post(
                    "http://localhost:8000/generate-fact",
                    json={"prompt": fact_prompt}
                )
                if response.status_code == 200:
                    st.success("Fact generated!")
                    st.markdown(response.json()["fact"])
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the server")
        else:
            st.warning("Please enter a prompt first!")

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and FastAPI")