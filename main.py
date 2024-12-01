import os
from tempfile import NamedTemporaryFile
import streamlit as st
from tools import ImageCaptionTool, ObjectDetectionTool
from Gemini import get_gemini_response

# Initialize tools
image_caption_tool = ImageCaptionTool()
object_detection_tool = ObjectDetectionTool()

# Streamlit App
st.title("Ask a Question About an Image")
st.header("Please upload an image")

# Upload file
file = st.file_uploader("", type=["jpeg", "jpg", "png"])

if file:
    # Save the uploaded file to a permanent path
    upload_folder = "uploads"  # You can change this path as needed
    os.makedirs(upload_folder, exist_ok=True)  # Create the folder if it doesn't exist
    file_path = os.path.join(upload_folder, file.name)
    
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    
    # Display the uploaded image
    st.image(file, use_column_width=True)

    # Process the uploaded image
    with st.spinner("Generating image captions..."):
        image_caption = image_caption_tool.run(file_path)
    st.write("Image Caption:", image_caption)

    with st.spinner("Detecting objects in the image..."):
        object_detection = object_detection_tool.run(file_path)
    st.write("Objects Detected:", object_detection)

    # Get user question
    user_question = st.text_input("Ask a question about your image:")

    if user_question:
        # Combine tool outputs and user question into a prompt
        prompt = (
            f"{user_question}\n\n"
            f"Image Caption: {image_caption}\n"
            f"Objects Detected: {object_detection}\n"
        )

        # Call Gemini manually
        with st.spinner("Getting response from Gemini..."):
            response = get_gemini_response(prompt)
        st.write("Gemini's Response:", response)
