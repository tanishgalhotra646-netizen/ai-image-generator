import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ----------------------------
# Streamlit Page Config
# ----------------------------

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 AI Image Generator")
st.write("Generate stunning AI images from text prompts.")

# ----------------------------
# Hugging Face API
# ----------------------------

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

# Read token from Streamlit Secrets
HF_TOKEN = st.secrets["HF_TOKEN"]

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# ----------------------------
# User Input
# ----------------------------

prompt = st.text_area(
    "Enter your prompt",
    placeholder="A futuristic city at sunset with flying cars..."
)

# ----------------------------
# Generate Image
# ----------------------------

if st.button("Generate Image"):

    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
        st.stop()

    with st.spinner("Generating image..."):

        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=300
        )

    if response.status_code == 200:

        image = Image.open(BytesIO(response.content))

        st.image(
            image,
            caption=prompt,
            use_container_width=True
        )

        buffer = BytesIO()
        image.save(buffer, format="PNG")

        st.download_button(
            "📥 Download Image",
            data=buffer.getvalue(),
            file_name="generated_image.png",
            mime="image/png"
        )

    else:

        st.error("Image generation failed.")
        st.code(response.text)
