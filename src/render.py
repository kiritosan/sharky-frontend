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


backend_url: str = os.getenv('BACKEND_URL', 'http://localhost:8000')
upload_images_url: str = backend_url + '/images'
history_url: str = backend_url + '/histories'
siren_url: str = 'https://crowdcount.oss-cn-hangzhou.aliyuncs.com/assets/siren2.mp3'
path: str = os.path.join(os.getcwd(), 'src', 'assets')
place_holder_path: str = os.path.join(path, 'placeholder.png')
error_path: str = os.path.join(path, 'error.png')
place_holder: ImageClass = Image.open(place_holder_path)


def render_main() -> None:
    # https://emojipedia.org/flower-playing-cards/
    imageTab: DeltaGenerator
    dataTab: DeltaGenerator
    imageTab, dataTab = st.tabs(["π΄ Image", "π Data"])

    with imageTab:
        st.header("π΄ Image")
        originalImgCol: DeltaGenerator
        processedImgCol: DeltaGenerator
        originalImgCol, processedImgCol = st.columns(2)
        # declared before spinner, so the spinner is under the columns
        uploaded_file: UploadedFile | None = st.file_uploader(
            "Upload Image", type=['jpg', 'jpeg', 'png'])

        # response logic can put anywhere unless there are a view need variables
        if uploaded_file is not None:
            filename = uploaded_file.name
            st.sidebar.info(f'εΎηε―Όε₯ζε')
        else:
            filename: Literal[''] = ""

        with originalImgCol:
            if uploaded_file is not None:
                image: ImageClass = Image.open(uploaded_file)
                st.image(
                    image, caption=f'Original Image: {filename}', use_column_width=True)
            else:
                st.image(place_holder, caption="Original Image",
                         use_column_width=True)

        # the snippet below couldn't be put in the with statement because the spinner will be under the columns
        if uploaded_file is not None:
            with st.spinner('θ―·η­εΎεΎηδΈδΌ εε€η...'):
                res: Response | None = upload_image_get_response(
                    uploaded_file, upload_images_url)
        else:
            res: Response | None = None

        with processedImgCol:
            if 'predict_digits' not in st.session_state:
                st.session_state['predict_digits'] = None
            bias = 0
            previous_predict_digits = 0

            if st.session_state['predict_digits'] is not None:
                previous_predict_digits: int = int(
                    st.session_state['predict_digits'][0])

            if res is not None:
                if res.status_code == 200 and 'message' not in res.json():
                    res_urls: list[str] = res.json()['processed_urls']
                    st.session_state['predict_digits'] = res.json()[
                        'predict_digits']
                    if previous_predict_digits is not None:
                        bias: int = st.session_state['predict_digits'][0] - int(
                            previous_predict_digits)
                    # face multiple images upload situation, but st.uploader only support upload one image at one time
                    for res_url in res_urls:
                        st.image(
                            res_url, caption=f"Processed Image: {filename}", use_column_width=True)

                elif res.status_code == 200 and res.json()['message'] == "the engine download pictures failed":
                    st.sidebar.error(f'εΌζδΈθ½½εΎηε€±θ΄₯οΌθ―·ιζ°δΈδΌ ')
                    error: ImageClass = Image.open(error_path)
                    st.image(error, caption="Processed Image",
                             use_column_width=True)

                elif res.status_code == 200 and res.json()['message'] == "the engine predict failed":
                    st.sidebar.error(f'εΌζι’ζ΅ε€±θ΄₯οΌθ―·ιζ©εΆδ»εΎηθΏθ‘ι’ζ΅')
                    error: ImageClass = Image.open(error_path)
                    st.image(error, caption="Processed Image",
                             use_column_width=True)

                elif res.status_code == 200 and res.json()['message'] == 'backend upload to oss failed':
                    st.sidebar.error(f'εη«―δΈδΌ εΎηε€±θ΄₯οΌθ―·ιζ°δΈδΌ ')
                    error: ImageClass = Image.open(error_path)
                    st.image(error, caption="Processed Image",
                             use_column_width=True)

                elif res.status_code == 200 and res.json()['message'] == 'the engine download pictures failed because the url is wrong':
                    st.sidebar.error(f'εΌζδΈθ½½εΎηε€±θ΄₯οΌε εη«―ζδΎη»εΌζηιΎζ₯δΈε­ε¨')
                    error: ImageClass = Image.open(error_path)
                    st.image(error, caption="Processed Image",
                             use_column_width=True)

                elif res.status_code == 200 and res.json()['message'] == 'the engine failed to upload processed file':
                    st.sidebar.error(f'εΌζδΈδΌ εΎηε€±θ΄₯')
                    error: ImageClass = Image.open(error_path)
                    st.image(error, caption="Processed Image",
                             use_column_width=True)
            else:
                st.image(place_holder, caption="Processed Image",
                         use_column_width=True)

        threshold: int = st.slider(
            'θ―·ιζ©θ­¦η€ΊιεΌοΌ', 0, 100, 10, key='state_threshold')
        st.markdown(f'ε½εηͺε£θΆθΏ `{threshold}` δΊΊεοΌη³»η»θΏθ‘δΊΊζ°ι’θ­¦')
        # switch for siren
        # state logic can put anywhere unless there are a view need variables
        if 'siren' not in st.session_state:
            st.session_state['siren'] = True
        button: bool = st.button('π ι’θ­¦')
        if button:
            st.session_state['siren'] = not st.session_state['siren']
        # siren hint view, need to be put after the button, before other views which need render after the hint
        if st.session_state['siren'] == True:
            st.write(f'π ι’θ­¦ζ­ζ₯οΌεΌ')
        else:
            st.write(f'π ι’θ­¦ζ­ζ₯οΌε³')

        if st.session_state['predict_digits'] is not None:
            for predict_digit in st.session_state['predict_digits']:
                if predict_digit >= threshold:
                    st.metric(label="ε½ει’ζ΅ζ°εΌ", value=predict_digit, delta=bias)
                    st.error(
                        f'ε½εηͺε£δΊΊζ°δΈΊ`{predict_digit}`δΊΊοΌε·²θΆθΏ `{threshold}` δΊΊοΌη³»η»θΏθ‘δΊΊζ°ι’θ­¦οΌθ―·ζ³¨ζοΌ', icon="β οΈ")
                    # TODO: HOW TO MAKE DOCKER work
                    # this link is sharky-backend:8000/static/siren2.mp3, browser can not play it
                    if st.session_state['siren']:
                        components.html(
                            """
                                <audio autoplay style:"visibility:hidden;position:fixed;">
                                    <source src="%s" type="audio/mpeg">
                                </audio>
                            """ % siren_url
                        )
                else:
                    st.metric(label="ε½ει’ζ΅ζ°εΌ", value=predict_digit, delta=bias)
                    st.success(
                        f'ε½εηͺε£δΊΊζ°δΈΊ`{predict_digit}`δΊΊοΌζͺθΆθΏ `{threshold}` δΊΊοΌθ―·η»§η»­δΏζ', icon="π")

    with dataTab:
        st.header("π Data")
        st.markdown("This is the data tab")


def render_history() -> None:
    st.header("π History")
    response: Response | None = get_history(history_url)
    if response:
        pd.set_option('display.max_colwidth', None)
        df = pd.DataFrame(response.json())
        chart_data = df[['create_time', 'crowd_predict_number']]
        chart_data['create_time'] = pd.to_datetime(chart_data['create_time'])

        st.line_chart(chart_data, x='create_time')
        st.table(df)
