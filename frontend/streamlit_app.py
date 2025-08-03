import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="Story Generator",
    page_icon="📚",
    layout="centered"
)

# Add title
st.title("✨ AI Story Generator")

# Create input field for story prompt
prompt = st.text_area("Enter your story prompt:", height=100)

# Create generate button
if st.button("Generate Story"):
    if prompt:
        try:
            # Call the FastAPI endpoint
            response = requests.post(
                "http://localhost:8000/generate-story",
                json={"prompt": prompt}
            )
            
            if response.status_code == 200:
                # Display the generated story
                story = response.json()["story"]
                st.success("Story generated successfully!")
                st.markdown("### Your Story:")
                st.write(story)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the server. Make sure the FastAPI backend is running.")
    else:
        st.warning("Please enter a prompt first!")

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and FastAPI")