import os
import streamlit as st
from basic_config import basic_config
from render import render_main, render_history
from streamlit.delta_generator import DeltaGenerator
from PIL import Image
from PIL.Image import Image as ImageClass

# Streamlit encourages well-structured code, like starting execution in a main() function.
def main() -> None:
    # Set basic config
    basic_config()
    path: str = os.path.join(os.getcwd(), "src", "assets", "logo.png")
    image: ImageClass = Image.open(path)
    logo: DeltaGenerator = st.sidebar.image(image, caption="SHARKY SYSTEM", use_column_width=True)
    # Set a Content Area to display the main content of the app.
    content: DeltaGenerator = st.markdown('Content Area', unsafe_allow_html=True)
    
    # Set sidebar
    app_mode: str | None = st.sidebar.radio("请选择计数模型", ["使用说明", "运行系统", "查看源码", "显示历史记录"])
    # TODO: delete+++++++++++++++++++++++++++++++++++++++=====================+++++++++++++++++++++++++++++++++++++++++++++++
    app_mode="显示历史记录"
    # Render the app based on the user selection.
    if app_mode == "使用说明":
        content.empty()
        readme_path: str = os.path.join(os.getcwd(), 'README.md')
        with open(readme_path, "r", encoding='UTF-8') as f:
            readme_content: str = f.read()
        content = st.markdown(readme_content, unsafe_allow_html=True)
        st.sidebar.success('选择运行系统进行人群计数')
    elif app_mode == "运行系统":
        content.empty()
        render_main()
    elif app_mode == "查看源码":
        content.empty()
        with open("src/main.py", "r", encoding='UTF-8') as f:
            source_code: str = f.read()
        st.code(source_code)
    elif app_mode == "显示历史记录":
        content.empty()
        render_history()

if __name__ == "__main__":
    main()