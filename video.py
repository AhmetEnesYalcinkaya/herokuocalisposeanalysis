"""Media streamings"""
import logging
from pathlib import Path
from typing import Dict, Optional, cast

import av
import cv2
import streamlit as st
from aiortc.contrib.media import MediaPlayer
from streamlit_webrtc import WebRtcMode, WebRtcStreamerContext, webrtc_streamer


def create_player():
    return MediaPlayer(str("image/video.mp4"))

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")

    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="deneme1",
    mode=WebRtcMode.RECVONLY,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}], "sdpSemantics": "unified-plan"},
    media_stream_constraints={
        "video": True,
    },
    player_factory=create_player,
    video_frame_callback=video_frame_callback,
)
