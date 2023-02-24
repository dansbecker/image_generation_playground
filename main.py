import streamlit as st
import openai
import os
import streamlit as st
from PIL import Image
import requests
import logging

default_prompt = "Describe the image you want to create"
@st.cache
def request_image(prompt, resolution_request, n_images):
    ip = get_remote_ip()
    logging.info(f"Requesting image. IP: {ip}\tprompt: {prompt}\ttresolution_request: {resolution_request}\tn_images: {n_images}")
    resp = openai.Image.create(
        prompt=prompt,
        size=resolution_request,
        n=n_images,
    )
    urls = [i['url'] for i in resp['data']]
    return urls

@st.cache
def get_image(url):
    img = Image.open(requests.get(url, stream = True).raw)
    return img

def get_remote_ip() -> str:
    """Get remote ip."""

    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    out = session_info.request.remote_ip
    print(out)
    return(out)

def is_valid_prompt(prompt):
    if prompt == "" or prompt == default_prompt:
        return False
    return True

openai.api_key = os.getenv("OPENAI_CLIENT_SECRET")

prompt1 = st.text_area(default_prompt)
image_size = st.selectbox("Image size", [512, 1024])
image_size_reqest = str(image_size) + "x" + str(image_size)
n_images = st.selectbox("Number of images", [1, 2, 3])
# streamlit multiselect for styles
if is_valid_prompt(prompt1):
    urls = request_image(prompt1, image_size_reqest, n_images)
    images = [get_image(url) for url in urls]
    for image in images:
        st.image(image, use_column_width=True)
