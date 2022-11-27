import os
import time
import requests
import streamlit as st
from PIL import Image
from basic_config import basic_config
from render_app import render_app

##########################################################################################

# Streamlit encourages well-structured code, like starting execution in a main() function.
def main():
    basic_config()
    
    content = st.markdown('Content Area', unsafe_allow_html=True)
    
    # set basic config; render readme; render source code; render sidebar

    # Set basic config

    # Set sidebar
    st.sidebar.title("Crowd Counting System")
    app_mode = st.sidebar.radio("请选择计数模型",
        ["使用说明", "运行系统", "查看源码", "显示历史记录"])

    # Render the app based on the user selection.
    if app_mode == "使用说明":
        content.empty()
        # Render the readme as markdown using st.markdown.
        with open("README.md", "r", encoding='UTF-8') as f:
            ReadmeContent = f.read()
        content = st.markdown(ReadmeContent, unsafe_allow_html=True)
        st.sidebar.success('选择运行系统进行人群计数')
    elif app_mode == "运行系统":
        content.empty()
        run_the_app()
    elif app_mode == "查看源码":
        content.empty()
        # Get the source code for the app
        with open("src/main.py", "r", encoding='UTF-8') as f:
            sourceCode = f.read()
        st.code(sourceCode)
    elif app_mode == "显示历史记录":
        content.empty()
        st.write("历史记录")

# This is the main app app itself, which appears when the user selects "Run the app".
def run_the_app():
    render_app()

if __name__ == "__main__":
    main()