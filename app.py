"""
Main app file.
"""
import streamlit as st
import cv2
import numpy as np
import os
from utils.variables import var
from PIL import Image
import time

st.set_page_config(layout="wide")

sidebar = st.sidebar
sidebar.markdown("## Modes ")

size_reducer = sidebar.checkbox("Image Size Reducer")

if size_reducer:
    st.markdown("## Selected Size Reducer")
    exts = var.allowed_modes_dict["Image Size Reducer"]["extensions"].split(",")
    uploaded_file = st.file_uploader(f"Select file: {exts}", type=exts)
    if uploaded_file is not None:
        fname = f"data/{int(time.time())}."+uploaded_file.name.split(".")[-1]

        img = Image.open(uploaded_file).convert("RGB")        
        with open(fname, "wb") as f:
            f.write(uploaded_file.getbuffer())
            for f in os.listdir("data"):
                ts = float(f.split(".")[0])
                try:
                    if time.time()-ts > 120:
                        os.remove("data/"+f)
                except:
                    pass

        img = np.asarray(img)
        H,W,_=img.shape        
        show_image = st.checkbox("Show Image")
        if show_image:
            st.image(img, use_column_width=True)
        
        
        st.markdown(f"""Original Dimension of the image is: {H,W}. \\
                        Original Size of the image is: {os.path.getsize(fname)/1024}kbs \\
                        Please Select H and W.""")
        
        cols = st.columns(2)
        h = cols[0].number_input("Height", min_value=1, value=int(H))
        w = cols[1].number_input("Width",min_value=1, value=int(W))

        if st.button("Reduce size!!"):
            nimg = cv2.resize(img, (int(w), int(h)), interpolation=cv2.INTER_AREA)
            nfname = fname.replace("data/", "data/temp_")
            
            nimg = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)

            if show_image:
                st.image(img, use_column_width=True)


            cv2.imwrite(nfname, nimg)
            st.markdown(f"New file size: {os.path.getsize(nfname)/1024} kbs")

            with open(nfname, "rb") as fp:
                dbtn = st.download_button(label="Download image file.", data=fp,
                            file_name=nfname.split("/")[-1], mime="image/png")
                if dbtn:
                    st.markdown("Downloaded!!!!")
else:
    st.markdown("## No Mode Selected!!")


