"""
Main app file.
"""
from email.mime import image
import streamlit as st
from utils.variables import var
from utils.utils import *

st.set_page_config(layout='wide', page_title="Image Online Tool",
                    page_icon="assets/icon.png",
                    menu_items={
                        'About': "# Image Online Tool!"
                })

sidebar = st.sidebar
sidebar.markdown("## Modes ")

mode_size_reducer = sidebar.checkbox("Image Size Reducer")
mode_image_merger = sidebar.checkbox("Image Merger")

remove_old()

if mode_size_reducer:
    st.markdown("## Selected Size Reducer")
    size_reducer(st)
if mode_image_merger:
    st.markdown("## Selected Image Merger")
    image_merger(st)
# st.file_uploader
# else:
#     st.markdown("## No Mode Selected!!")


