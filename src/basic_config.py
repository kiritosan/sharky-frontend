import streamlit as st
from PIL import Image
from PIL.Image import Image as ImageClass

def basic_config() -> None:
    image:ImageClass = Image.open("C:\\Users\\Willem\\Desktop\\Course_Project\\crowd-counting\\frontend\\src\\assets\\favicon.png")
    st.set_page_config(
        page_title="SHARKY SYSTEM",
        # page_icon="🦈",
        page_icon=image,
        layout="wide",
        initial_sidebar_state="expanded",
    )