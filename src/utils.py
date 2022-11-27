import requests
import streamlit as st

# return assert's path or none
def request_processed_image_url(uploaded_file):
    url = "http://localhost:8000/images/"
    headers = {
        'accept': 'application/json',
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
    }

    if uploaded_file is not None:

        files = {
            'files': (uploaded_file.filename ,uploaded_file.getvalue(), 'image/jpeg'),
        }

        response = requests.request('POST', url, headers=headers, files=files)

        if response.status_code == 200:
            st.sidebar.success(f'上传成功\n{response}')
        else:
            st.sidebar.error(f'上传失败\n{response}')

        return response.json()['url']
    else:
        return None