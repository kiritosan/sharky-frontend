import os
import streamlit as st
from PIL import Image
from PIL.Image import Image as ImageClass

def basic_config() -> None:
    path: str = os.path.join(os.getcwd(), "src", "assets", "favicon.png")
    image:ImageClass = Image.open(path)
    st.set_page_config(
        page_title="SHARKY SYSTEM",
        page_icon=image,
        layout="wide",
        initial_sidebar_state="expanded",
    )