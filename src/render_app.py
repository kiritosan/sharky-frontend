import streamlit as st
from PIL import Image
from utils import request_processed_image_url
# from streamlit import UploadedFile

def render_app():
        # https://emojipedia.org/flower-playing-cards/
        imageTab, dataTab = st.tabs(["🎴 Image", "🗃 Data"])

        with imageTab:
            st.header("🎴 Image")
            originalImgCol, processedImgCol = st.columns(2)
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file is not None:
                filename = uploaded_file.filename
            else:
                filename = ""

            with originalImgCol:
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=f'Original Image: {filename}', use_column_width=True)
                else:
                    # TODO: Show a default image.
                    st.image("https://i.imgur.com/6jK6Y1r.jpg", caption="Original Image", use_column_width=True)
            with processedImgCol:
                if uploaded_file is not None:
                    st.sidebar.warning(uploaded_file.filename)
                returned_url = request_processed_image_url(uploaded_file)
                if returned_url is not None:
                    st.sidebar.success(returned_url)
                    # st.image(image, caption='Processed Image', use_column_width=True)
                    st.image(returned_url, caption="Processed Image", use_column_width=True)
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