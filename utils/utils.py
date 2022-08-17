"""

"""
from utils.variables import var
from PIL import Image
import time, os, io
import numpy as np
import cv2

def remove_old():
    for f in os.listdir("data"):
        if "temp" in f:        
            ts = float(f.split(".")[0].split("_")[-1])
        else:
            ts = float(f.split(".")[0])
        try:
            if time.time()-ts > 60:
                os.remove("data/"+f)
        except:
            pass

def size_reducer(st):
    exts = var.allowed_modes_dict["Image Size Reducer"]["extensions"].split(",")
    uploaded_file = st.file_uploader(f"Select file: {exts}", type=exts)
    if uploaded_file is not None:
        fname = f"data/{int(time.time())}."+uploaded_file.name.split(".")[-1]

        img = Image.open(uploaded_file).convert("RGB")        
        with open(fname, "wb") as f:
            f.write(uploaded_file.getbuffer())
            

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

def image_merger(st):
    exts = var.allowed_modes_dict["Image Merger"]["extensions"].split(",")
    
    show_image = st.checkbox("Show Image")
    merge_horizontally = st.checkbox("Merge Horizontally")
    margin = st.number_input("Margin between two images.", value=10)

    all_imgs = {}
    uploaded_file = st.file_uploader(f"Select file: {exts}", type=exts, accept_multiple_files=True)
    files = []

    if uploaded_file is not None:
        nh=0
        nw=0
        for uf in uploaded_file:
            fname = f"data/{int(time.time())}."+uf.name #.split(".")[-1]
            
            bd = uf.read()

            img = Image.open(io.BytesIO(bd)).convert("RGB")        
            with open(fname, "wb") as f:
                f.write(uf.getbuffer())
                
            img = np.asarray(img)
            H,W,_=img.shape        
            
            nh+=H
            nw+=W

            if show_image:
                st.markdown(f"### {uf.name}")
                st.image(img, use_column_width=True)

            files.append(fname)
            # all_imgs[fname] = img

    if len(files)>0:
        # st.write(files)
        fs=len(uploaded_file)
        nh = int(nh/fs)
        nw = int(nw/fs)
        
        if merge_horizontally:
            mr = np.zeros((nh, int(margin), 3))+255.0
        else:
            mr = np.zeros((int(margin), nw, 3))+255.0

        nimg = None
        for file in files:
            img = cv2.imread(file)
            img = img[:,:,::-1]

            img = cv2.resize(img, (nw, nh))
            # st.image(img)
            
            # st.image(mr)
            if nimg is None:
                nimg = img.copy()
                nimg = nimg.astype(np.uint8)
                # st.image(nimg, use_column_width=True)
            else:
                if merge_horizontally:
                    nimg = np.hstack([nimg, mr, img])
                else:
                    nimg = np.vstack([nimg, mr, img])

                nimg = nimg.astype(np.uint8)
                # st.image(nimg, use_column_width=True)
        
        st.markdown("### Merged Image")
        st.image(nimg, use_column_width=True) 


        nfname=f"data/temp_{int(time.time())}.png"
        cv2.imwrite(nfname, nimg[:,:,::-1])

        with open(nfname, "rb") as fp:
            dbtn = st.download_button(label="Download image file.", data=fp,
                        file_name=nfname.split("/")[-1], mime="image/png")
            if dbtn:
                st.markdown("Downloaded!!!!")


    