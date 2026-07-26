import streamlit as st
import torch
from diffusers import StableDiffusionPipeline

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 AI Image Generator")
st.write("Generate images using Stable Diffusion v1.5")

# Load model only once
@st.cache_resource
def load_model():

    model_id = "runwayml/stable-diffusion-v1-5"

    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float32
    )

    pipe = pipe.to("cpu")     # Change to cuda if GPU available

    return pipe

pipe = load_model()

prompt = st.text_input(
    "Enter your prompt",
    placeholder="A futuristic city at sunset"
)

if st.button("Generate Image"):

    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:

        with st.spinner("Generating image..."):

            image = pipe(prompt).images[0]

        st.image(image, caption=prompt, use_container_width=True)

        image.save("generated_image.png")

        with open("generated_image.png", "rb") as file:

            st.download_button(
                label="Download Image",
                data=file,
                file_name="generated_image.png",
                mime="image/png"
            )