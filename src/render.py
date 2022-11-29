import os
import streamlit as st
from PIL import Image
from PIL.Image import Image as ImageClass
from utils import upload_image_get_response
from typing import Literal
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.uploaded_file_manager import UploadedFile
from requests.models import Response

url: str = os.getenv('URL', 'http://localhost:8000/images')

def render() -> None:
        # https://emojipedia.org/flower-playing-cards/
        imageTab: DeltaGenerator; dataTab:DeltaGenerator
        imageTab, dataTab = st.tabs(["🎴 Image", "🗃 Data"])

        with imageTab:
            st.header("🎴 Image")
            originalImgCol: DeltaGenerator; processedImgCol: DeltaGenerator
            originalImgCol, processedImgCol = st.columns(2)
            uploaded_file: UploadedFile | None = st.file_uploader("Choose a file")
            if uploaded_file is not None:
                filename = uploaded_file.name
            else:
                filename: Literal[''] = ""

            with originalImgCol:
                if uploaded_file is not None:
                    image: ImageClass = Image.open(uploaded_file)
                    st.image(image, caption=f'Original Image: {filename}', use_column_width=True)
                else:
                    # TODO: Show a default image.
                    st.image("https://i.imgur.com/6jK6Y1r.jpg", caption="Original Image", use_column_width=True)
            with processedImgCol:
                if uploaded_file is not None:
                    st.sidebar.info(f'图片导入成功')
                res: Response | None = upload_image_get_response(uploaded_file, url)
                if res is not None:
                    if res.status_code == 200:
                        res_urls: str = res.json()['original_url']
                        for res_url in res_urls:
                            st.image(res_url, caption="Processed Image", use_column_width=True)
                    else:
                        ...
                else:
                    # TODO: Show a default image.
                    st.image("https://i.imgur.com/6jK6Y1r.jpg", caption="Processed Image", use_column_width=True)

            num: int = st.slider('请选择警示阈值：', 0, 100, 10)
            st.markdown(f'当前窗口超过 `{num}` 人后，系统进行人数预警')

            testDate: int = st.slider('请选择测试人数：', 0, 100, 10)
            if(testDate > num):
                st.warning(f'人数超过{num}人，请注意！', icon="⚠️")
            
        with dataTab:
            st.header("🗃 Data")
            st.markdown("This is the data tab")