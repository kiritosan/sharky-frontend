import requests
import streamlit as st
from requests.models import Response
from streamlit.runtime.uploaded_file_manager import UploadedFile
from typing import Literal

# return assert's path or none
def upload_image_get_response(uploaded_file: UploadedFile | None, url: str) -> Response | None:
    headers: dict[str, str] = {
        'accept': 'application/json',
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
    }

    if uploaded_file is not None:
        st.sidebar.info(f'开始上传图片进行处理')

        files: dict[str, tuple[str, bytes, Literal['image/jpeg']]] = {
            'files': (uploaded_file.name ,uploaded_file.getvalue(), 'image/jpeg'),
        }

        response: Response = requests.request('POST', url, headers=headers, files=files)

        if response.status_code == 200:
            st.sidebar.success(f'处理完成 请等待资源载入')
        else:
            st.sidebar.error(f'上传失败, 请重试')

        return response
    else:
        return None