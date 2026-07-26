import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from urllib.parse import quote

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 AI Image Generator")
st.write("Generate AI images from text prompts using Pollinations AI.")

prompt = st.text_area(
    "Enter your prompt",
    placeholder="A futuristic city at sunset with flying cars..."
)

width = st.selectbox("Width", [512, 768, 1024], index=0)
height = st.selectbox("Height", [512, 768, 1024], index=0)

if st.button("Generate Image"):

    if not prompt.strip():
        st.warning("Please enter a prompt.")
        st.stop()

    with st.spinner("Generating image..."):

        url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width={width}&height={height}&nologo=true"

        try:
            response = requests.get(url, timeout=120)
            response.raise_for_status()

            image = Image.open(BytesIO(response.content))

            st.image(image, caption=prompt, use_container_width=True)

            buffer = BytesIO()
            image.save(buffer, format="PNG")

            st.download_button(
                "📥 Download Image",
                buffer.getvalue(),
                "generated_image.png",
                "image/png"
            )

        except Exception as e:
            st.error(f"Error: {e}")
