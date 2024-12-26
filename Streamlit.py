import streamlit as st
import httpx
import base64
import os
from dotenv import load_dotenv
import google.generativeai as genai1

# Load environment variables from .env file
load_dotenv()

# Configure the API key for Google Generative AI
api_key = os.getenv("GOOGLE_API_KEY")
genai1.configure(api_key=api_key)

# Initialize the model
model = genai1.GenerativeModel(model_name="gemini-1.5-pro")

# Streamlit UI setup
st.title("Text Extraction Using Gemini")

st.markdown("""
Upload an image, and we will generate a caption or description based on the image using the Gemini model.
""")

# Image upload
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

# If an image is uploaded, display the image and initiate the conversation
if uploaded_file is not None:
    # Display the uploaded image
    image = uploaded_file
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Convert the image to base64
    img_bytes = image.read()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    # Initialize conversation history
    conversation = []

    # Text input for additional user input prompt (as chat input)
    user_input = st.chat_input("Enter a description prompt:")

    if user_input:
        # Add user message to conversation history
        conversation.append({"role": "user", "message": user_input})

        # Display user message
        st.chat_message("user").write(user_input)
        
        with st.spinner("Generating description..."):
            try:
                # Call the model to generate content based on the image and user input
                response = model.generate_content([{'mime_type': 'image/jpeg', 'data': img_base64}, user_input])
                
                # Display assistant's response
                assistant_response = response.text
                conversation.append({"role": "assistant", "message": assistant_response})
                
                # Show assistant's message in the chat
                st.chat_message("assistant").write(assistant_response)
                
            except Exception as e:
                st.error(f"Error generating caption: {e}")
    else:
        st.warning("Please provide a description prompt to guide the generation.")
