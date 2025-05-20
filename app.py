import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image

# Load color dataset
@st.cache_data
def load_colors():
    df = pd.read_csv("colors.csv", usecols=["color_name", "R", "G", "B"])
    return df

# Get closest color name
def get_closest_color_name(R, G, B, df):
    diff = np.sqrt((df["R"] - R)**2 + (df["G"] - G)**2 + (df["B"] - B)**2)
    index = diff.idxmin()
    return df.loc[index, "color_name"], (df.loc[index, "R"], df.loc[index, "G"], df.loc[index, "B"])

# Streamlit app
st.title("🎨 Color Detection from Image")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
df_colors = load_colors()

if uploaded_file:
    image = Image.open(uploaded_file)
    image = np.array(image)
    st.image(image, caption="Uploaded Image")

    st.markdown("**Click 'Detect Color' and select a pixel in the new window**")

    if st.button("Detect Color"):
        # Resize for OpenCV if too large
        img_resized = cv2.resize(image, (600, 400))

        clicked = {}

        def click_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                b, g, r = img_resized[y, x]
                clicked['color'] = (r, g, b)
                clicked['pos'] = (x, y)
                cv2.destroyAllWindows()

        cv2.imshow("Click to detect color", img_resized)
        cv2.setMouseCallback("Click to detect color", click_event)
        cv2.waitKey(0)

        if 'color' in clicked:
            r, g, b = clicked['color']
            color_name, (cr, cg, cb) = get_closest_color_name(r, g, b, df_colors)

            st.markdown(f"**Detected Color:** {color_name}")
            st.markdown(f"**RGB:** ({cr}, {cg}, {cb})")
            st.markdown(
                f"<div style='width:100px; height:50px; background-color: rgb({cr},{cg},{cb});'></div>",
                unsafe_allow_html=True
            )
