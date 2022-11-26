import os
import time
import streamlit as st
from PIL import Image

##########################################################################################

# Streamlit encourages well-structured code, like starting execution in a main() function.
def main():
    readme_text = None
    sourceCode = None
    app_mode = None
    
    # set basic config; render readme; render source code; render sidebar

    # Set basic config
    basic_config()

    # Render the readme as markdown using st.markdown.
    with open("README.md", "r", encoding='UTF-8') as f:
        ReadmeContent = f.read()
    readme_text = st.markdown(ReadmeContent, unsafe_allow_html=True)

    # Get the source code for the app
    with open("frontend/__init__.py", "r", encoding='UTF-8') as f:
        sourceCode = f.read()

    # Set sidebar
    st.sidebar.title("Crowd Counting System")
    app_mode = st.sidebar.radio("请选择计数模型",
        ["使用说明", "运行系统", "查看源码", "显示历史记录"])

    # Render the app based on the user selection.
    if app_mode == "使用说明":
        st.sidebar.success('选择运行系统进行人群计数')
    elif app_mode == "查看源码":
        readme_text.empty()
        st.code(sourceCode)
    elif app_mode == "运行系统":
        readme_text.empty()
        run_the_app()
    elif app_mode == "显示历史记录":
        readme_text.empty()
        st.write("历史记录")

def basic_config():
    st.set_page_config(
        page_title="人群计数系统",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

# This is the main app app itself, which appears when the user selects "Run the app".
def run_the_app():

    def init():
        # https://emojipedia.org/flower-playing-cards/
        imageTab, dataTab = st.tabs(["🎴 Image", "🗃 Data"])

        with imageTab:
            st.header("🎴 Image")
            originalImgCol, processedImgCol = st.columns(2)
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file is not None:
                filename = uploaded_file.name
            else:
                filename = ""
            returned_file = run_model_get_result(uploaded_file, filename)

            with originalImgCol:
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=f'Original Image: {filename}', use_column_width=True)
                else:
                    # TODO: Show a default image.
                    st.image("https://i.imgur.com/6jK6Y1r.jpg", caption="Original Image", use_column_width=True)
            with processedImgCol:
                if returned_file is not None:
                    image = Image.open(returned_file)
                    st.image(image, caption='Processed Image', use_column_width=True)
                else:
                    # TODO: Show a default image.
                    st.image("https://i.imgur.com/6jK6Y1r.jpg", caption="Processed Image", use_column_width=True)

            num = st.slider('请选择警示阈值：', 0, 100, 10)
            st.write("当前窗口超过", num, '人后，系统进行人数预警')

            testDate = st.slider('请选择测试人数：', 0, 100, 10)

            if(testDate > num):
                st.warning(f'人数超过{num}人，请注意！', icon="⚠️")
            

        with dataTab:
            st.header("🗃 Data")
 
            st.write("This is the data tab")

    # return assert's path or none
    def run_model_get_result(uploaded_file, filename):
        if uploaded_file is not None:
            return os.path.abspath(os.path.join(os.getcwd(), "data", "processed", filename))
        else:
            return None

    init()

if __name__ == "__main__":
    main()