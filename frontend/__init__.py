import streamlit as st
import pandas as pd
import numpy as np
import os
import urllib
from PIL import Image
import time

##########################################################################################

# Streamlit encourages well-structured code, like starting execution in a main() function.
def main():
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
    app_mode = st.sidebar.selectbox("请选择计数模型",
        ["使用说明", "运行系统", "查看源码", "显示历史记录"])
    if app_mode == "使用说明":
        st.sidebar.success('选择运行系统进行人群计数')

        st.warning('This is a warning', icon="⚠️")

        age = st.slider('请选择警示阈值：', 0, 100, 10)
        st.write("当前窗口超过", age, '人后，系统进行人数预警')

        
        my_bar = st.progress(0)

        with st.spinner('Wait for it...'):
            time.sleep(3)
            # 代码运算
        st.success('Done!')
        st.success('This is a success', icon="🎉")


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
        initial_sidebar_state="collapsed",
        # menu_items={
        #     'Get Help': 'https://www.extremelycoolapp.com/help',
        #     'Report a bug': "https://www.extremelycoolapp.com/bug",
        #     'About': "# This is a header. This is an *extremely* cool app!"
        # }
    )




# This is the main app app itself, which appears when the user selects "Run the app".
def run_the_app():

    def init():
        # # Load the model.
        # st.write("Loading model...")
        # global model
        # model = ObjectDetector()
        # st.write("Model loaded!")

        # # Load the summary.
        # st.write("Loading summary...")
        # global summary
        # summary = pd.read_csv("summary.csv")
        # st.write("Summary loaded!")

        # https://emojipedia.org/flower-playing-cards/
        imageTab, dataTab = st.tabs(["🎴 Image", "🗃 Data"])

        with imageTab:
            st.header("🎴 Image")
            originalImgCol, processedImgCol = st.columns(2)
            uploaded_file = st.file_uploader("Choose a file")
            returned_file = run_model_get_result(uploaded_file)

            with originalImgCol:              
                if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    st.image(image, caption='Original Image', use_column_width=True)
                else:
                    st.image("https://i.imgur.com/6jK6Y1r.jpg", caption="Original Image", use_column_width=True)
            with processedImgCol:
                if returned_file is not None:
                    image = Image.open(returned_file)
                    st.image(image, caption='Original Image', use_column_width=True)
                else:
                    st.image("https://i.imgur.com/6jK6Y1r.jpg", caption="Processed Image", use_column_width=True)

            
        with dataTab:
            st.header("🗃 Data")
 
            st.write("This is the data tab")
            
        if st.button('process'):
            uploaded_file = True
        else:
            st.write('按下按钮进行计数')
        
        
    # To make Streamlit fast, st.cache allows us to reuse computation across runs.
    # In this common pattern, we download data from an endpoint only once.
    @st.experimental_memo
    def load_metadata(url):
        return pd.read_csv(url)

    # This function uses some Pandas magic to summarize the metadata Dataframe.
    @st.experimental_memo
    def create_summary(metadata):
        one_hot_encoded = pd.get_dummies(metadata[["frame", "label"]], columns=["label"])
        summary = one_hot_encoded.groupby(["frame"]).sum().rename(columns={
            "label_biker": "biker",
            "label_car": "car",
            "label_pedestrian": "pedestrian",
            "label_trafficLight": "traffic light",
            "label_truck": "truck"
        })
        return summary

    def run_model_get_result(uploaded_file1):
        if uploaded_file1 is not None:
            return os.path.abspath(os.path.join(os.getcwd(), "data", "processed", "processed.png"))
        else:
            return None

    init()








# This sidebar UI is a little search engine to find certain object types.
def frame_selector_ui(summary):
    st.sidebar.markdown("# Frame")

    # The user can pick which type of object to search for.
    object_type = st.sidebar.selectbox("Search for which objects?", summary.columns, 2)

    # The user can select a range for how many of the selected objecgt should be present.
    min_elts, max_elts = st.sidebar.slider("How many %ss (select a range)?" % object_type, 0, 25, [10, 20])
    selected_frames = get_selected_frames(summary, object_type, min_elts, max_elts)
    if len(selected_frames) < 1:
        return None, None

    # Choose a frame out of the selected frames.
    selected_frame_index = st.sidebar.slider("Choose a frame (index)", 0, len(selected_frames) - 1, 0)

    # Draw an altair chart in the sidebar with information on the frame.
    objects_per_frame = summary.loc[selected_frames, object_type].reset_index(drop=True).reset_index()
    chart = alt.Chart(objects_per_frame, height=120).mark_area().encode(
        alt.X("index:Q", scale=alt.Scale(nice=False)),
        alt.Y("%s:Q" % object_type))
    selected_frame_df = pd.DataFrame({"selected_frame": [selected_frame_index]})
    vline = alt.Chart(selected_frame_df).mark_rule(color="red").encode(x = "selected_frame")
    st.sidebar.altair_chart(alt.layer(chart, vline))

    selected_frame = selected_frames[selected_frame_index]
    return selected_frame_index, selected_frame

# Select frames based on the selection in the sidebar
@st.cache(hash_funcs={np.ufunc: str})
def get_selected_frames(summary, label, min_elts, max_elts):
    return summary[np.logical_and(summary[label] >= min_elts, summary[label] <= max_elts)].index

# This sidebar UI lets the user select parameters for the YOLO object detector.
def object_detector_ui():
    st.sidebar.markdown("# Model")
    confidence_threshold = st.sidebar.slider("Confidence threshold", 0.0, 1.0, 0.5, 0.01)
    overlap_threshold = st.sidebar.slider("Overlap threshold", 0.0, 1.0, 0.3, 0.01)
    return confidence_threshold, overlap_threshold

# Draws an image with boxes overlayed to indicate the presence of cars, pedestrians etc.
def draw_image_with_boxes(image, boxes, header, description):
    # Superpose the semi-transparent object detection boxes.    # Colors for the boxes
    LABEL_COLORS = {
        "car": [255, 0, 0],
        "pedestrian": [0, 255, 0],
        "truck": [0, 0, 255],
        "trafficLight": [255, 255, 0],
        "biker": [255, 0, 255],
    }
    image_with_boxes = image.astype(np.float64)
    for _, (xmin, ymin, xmax, ymax, label) in boxes.iterrows():
        image_with_boxes[int(ymin):int(ymax),int(xmin):int(xmax),:] += LABEL_COLORS[label]
        image_with_boxes[int(ymin):int(ymax),int(xmin):int(xmax),:] /= 2

    # Draw the header and image.
    st.subheader(header)
    st.markdown(description)
    st.image(image_with_boxes.astype(np.uint8), use_column_width=True)


# This function loads an image from Streamlit public repo on S3. We use st.cache on this
# function as well, so we can reuse the images across runs.
@st.experimental_memo(show_spinner=False)
def load_image(url):
    with urllib.request.urlopen(url) as response:
        image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = image[:, :, [2, 1, 0]] # BGR -> RGB
    return image

# Run the YOLO model to detect objects.
def yolo_v3(image, confidence_threshold, overlap_threshold):
    # Load the network. Because this is cached it will only happen once.
    @st.cache(allow_output_mutation=True)
    def load_network(config_path, weights_path):
        net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        output_layer_names = net.getLayerNames()
        output_layer_names = [output_layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        return net, output_layer_names
    net, output_layer_names = load_network("yolov3.cfg", "yolov3.weights")

    # Run the YOLO neural net.
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layer_names)

    # Supress detections in case of too low confidence or too much overlap.
    boxes, confidences, class_IDs = [], [], []
    H, W = image.shape[:2]
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > confidence_threshold:
                box = detection[0:4] * np.array([W, H, W, H])
                centerX, centerY, width, height = box.astype("int")
                x, y = int(centerX - (width / 2)), int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_IDs.append(classID)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, overlap_threshold)

    # Map from YOLO labels to Udacity labels.
    UDACITY_LABELS = {
        0: 'pedestrian',
        1: 'biker',
        2: 'car',
        3: 'biker',
        5: 'truck',
        7: 'truck',
        9: 'trafficLight'
    }
    xmin, xmax, ymin, ymax, labels = [], [], [], [], []
    if len(indices) > 0:
        # loop over the indexes we are keeping
        for i in indices.flatten():
            label = UDACITY_LABELS.get(class_IDs[i], None)
            if label is None:
                continue

            # extract the bounding box coordinates
            x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]

            xmin.append(x)
            ymin.append(y)
            xmax.append(x+w)
            ymax.append(y+h)
            labels.append(label)

    boxes = pd.DataFrame({"xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax, "labels": labels})
    return boxes[["xmin", "ymin", "xmax", "ymax", "labels"]]

# Path to the Streamlit public S3 bucket
DATA_URL_ROOT = "https://streamlit-self-driving.s3-us-west-2.amazonaws.com/"

# External files to download.
EXTERNAL_DEPENDENCIES = {
    "yolov3.weights": {
        "url": "https://pjreddie.com/media/files/yolov3.weights",
        "size": 248007048
    },
    "yolov3.cfg": {
        "url": "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg",
        "size": 8342
    }
}

if __name__ == "__main__":
    main()