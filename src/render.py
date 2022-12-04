import os
import streamlit as st
from PIL import Image
from PIL.Image import Image as ImageClass
from utils import upload_image_get_response, get_history
from typing import Literal
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.uploaded_file_manager import UploadedFile
from requests.models import Response
import streamlit.components.v1 as components
import pandas as pd


url: str = os.getenv('URL', 'http://localhost:8000')
images_url: str = url + '/images'
history_url: str = url + '/histories'
siren_url: str = url + '/static/siren2.mp3'
path: str = os.path.join(os.getcwd(), 'src', 'assets')
place_holder_path: str = os.path.join(path, 'placeholder.png')
error_path: str = os.path.join(path, 'error.png')
place_holder: ImageClass = Image.open(place_holder_path)

def render_main() -> None:
        # https://emojipedia.org/flower-playing-cards/
        imageTab: DeltaGenerator; dataTab:DeltaGenerator
        imageTab, dataTab = st.tabs(["🎴 Image", "🗃 Data"])

        with imageTab:
            st.header("🎴 Image")
            originalImgCol: DeltaGenerator; processedImgCol: DeltaGenerator
            originalImgCol, processedImgCol = st.columns(2)
            # declared before spinner, so the spinner is under the columns
            uploaded_file: UploadedFile | None = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])
            
            # response logic can put anywhere unless there are a view need variables
            if uploaded_file is not None:
                filename = uploaded_file.name
                st.sidebar.info(f'图片导入成功')
            else:
                filename: Literal[''] = ""

            with originalImgCol:
                if uploaded_file is not None:
                    image: ImageClass = Image.open(uploaded_file)
                    st.image(image, caption=f'Original Image: {filename}', use_column_width=True)
                else:
                    st.image(place_holder, caption="Original Image", use_column_width=True)
            
            # the snippet below couldn't be put in the with statement because the spinner will be under the columns
            if uploaded_file is not None:
                with st.spinner('请等待图片上传及处理...'):
                    res: Response | None = upload_image_get_response(uploaded_file, images_url)
            else:
                res: Response | None = None
                
            with processedImgCol:
                predict_digits: list[int] | None = None
                
                if res is not None:
                    if res.status_code == 200:
                        res_urls: str = res.json()['original_url']
                        predict_digits = res.json()['predict_digits']
                        # face multiple images upload situation, but st.uploader only support upload one image at one time
                        for res_url in res_urls:
                            st.image(res_url, caption="Processed Image", use_column_width=True)
                    else:
                        error: ImageClass = Image.open(error_path)
                        st.image(error, caption="Processed Image", use_column_width=True)
                else:
                    st.image(place_holder, caption="Processed Image", use_column_width=True)
                    
            threshold: int = st.slider('请选择警示阈值：', 0, 100, 10)
            st.markdown(f'当前窗口超过 `{threshold}` 人后，系统进行人数预警')

            if predict_digits is not None:
                for predict_digit in predict_digits:
                    if predict_digit >= threshold:
                        st.metric(label="当前预测数值", value=predict_digit, delta="0")
                        st.error(f'当前窗口人数为`{predict_digit}`人，已超过 `{threshold}` 人，系统进行人数预警，请注意！', icon="⚠️")

                        # TODO: HOW TO MAKE DOCKER work
                        # this link is sharky-backend:8000/static/siren2.mp3, browser can not play it
                        components.html(
                            """
                            <audio autoplay style:"visibility:hidden;position:fixed;">
                                <source src="%s" type="audio/mpeg">
                            </audio>
                            """ % siren_url
                        )
                    else:
                        st.metric(label="当前预测数值", value=predict_digit, delta="0")
                        st.success(f'当前窗口人数为`{predict_digit}`人，未超过 `{threshold}` 人，请继续保持', icon="👍")

        with dataTab:
            st.header("🗃 Data")
            st.markdown("This is the data tab")
            
def render_history() -> None:
    st.header("📜 History")
    response: Response | None = get_history(history_url)
    if response:
        pd.set_option('display.max_colwidth', None)
        # chart_data = pd.DataFrame(response.json(), columns=['predict_digits'])
        df = pd.DataFrame(response.json())
        chart_data = df[['create_time', 'crowd_predict_number']]
        chart_data['create_time'] = pd.to_datetime(chart_data['create_time'])

        st.line_chart(chart_data, x = 'create_time')
        st.table(df)
    