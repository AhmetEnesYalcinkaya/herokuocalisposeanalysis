import logging
import queue
from pathlib import Path
import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from streamlit_webrtc import (RTCConfiguration,VideoProcessorBase, WebRtcMode,webrtc_streamer,)
import streamlit as st
import mediapipe as mp
from PIL import Image
import tempfile
import av
import time
import math as m
import matplotlib.pyplot as plt
import asyncio

#Streamlit
st.set_page_config(
   page_title="Ocalis Pose Analysis App",
   page_icon="🎈")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
st.set_option('deprecation.showfileUploaderEncoding', False)


image = Image.open('image/ocalis.png')

st.image(image)

#Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=2)

flag = False
# Calculate distance
def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

def calculate(l_shoulder_y , l_wrist_y):
    print(l_shoulder_y,l_wrist_y)
    if l_shoulder_y > l_wrist_y:
        start_time = time.time()
        #print(start_time)


def form(path):
    pass

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    image = frame.to_ndarray(format="bgr24")
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        try:
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            h, w = image.shape[:2]
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            #For calculate
            lm = results.pose_landmarks
            lmPose  = mp_pose.PoseLandmark

            l_shoulder_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
            l_shoulder_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
            
            l_wrist_x = int(lm.landmark[lmPose.LEFT_WRIST].x * w)
            l_wrist_y = int(lm.landmark[lmPose.LEFT_WRIST].y * h)

            r_wrist_x = int(lm.landmark[lmPose.RIGHT_WRIST].x * w)
            r_wrist_y = int(lm.landmark[lmPose.RIGHT_WRIST].y * h)

            calculate(l_shoulder_y , l_wrist_y)
            #offset = findDistance(l_shoulder_x, l_shoulder_y, l_wrist_x, l_wrist_y)
            #print(offset)

            if l_shoulder_y > l_wrist_y:
                cv2.circle(image, (l_wrist_x,l_wrist_y), 20, (0, 0, 255), -1) #red
                cv2.circle(image, (l_shoulder_x,l_shoulder_y), 20, (0, 0, 255), -1) # red
            elif l_shoulder_y == l_wrist_y:
                cv2.circle(image, (l_wrist_x,l_wrist_y), 20, (255, 255, 0), -1) #yellow
                cv2.circle(image, (l_shoulder_x,l_shoulder_y), 20, (255, 255, 0), -1) #yellow
            else:
                cv2.circle(image, (l_wrist_x,l_wrist_y), 20, (0, 255, 0), -1) #green
                cv2.circle(image, (l_shoulder_x,l_shoulder_y), 20, (0, 255, 0), -1) #green

            #Mediapipe
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            
            return av.VideoFrame.from_ndarray(image, format="bgr24")
            
        except:
            #print("helooo")
            st.markdown("Kameranin önüne geçiniz!")
            return av.VideoFrame.from_ndarray(image, format="bgr24")

if __name__ == "__main__":
    
    webrtc_ctx = webrtc_streamer(   
        key="deneme",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}], "sdpSemantics": "unified-plan"},
        #rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}],"sdpSemantics": "unified-plan"},
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True},
        async_processing=True,
        translations={
            "start": "👆 Start video recording",
            "stop": "Stop Analyze",})
    

    analysis = st.checkbox('📝 Show the analysis results')

    if analysis:
        option = st.selectbox('Choose sector name',('Automotive', 'Metal Production', 'Construction',"Plastic","Food"))
        if option:
            with st.spinner('⏳ Wait for analysis...'):
                time.sleep(3)
                st.success('💪 Analysis Completed!')

                ### 
                labels = 'True', 'False'
                sizes = [40,60]

                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                
                col1, col2 = st.columns([1, 1])

                image = Image.open('image/pose.png')
                col1.image(image)
                col2.pyplot(fig1)
                
                ###
                labels = 'True', 'False'
                sizes = [40,60]

                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                
                col1, col2 = st.columns([1, 1])

                image = Image.open('image/pose.png')
                col1.image(image)
                col2.pyplot(fig1)
        
                if st.button('📧 Send an e-mail as pdf'):
                    form('example.pdf')


        