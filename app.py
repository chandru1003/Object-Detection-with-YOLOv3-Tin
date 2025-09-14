import streamlit as st
import requests
from PIL import Image
import io
import base64

st.title("🖼️ Object Detection UI")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Show uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("🔍 Detect Objects"):
        files = {"file": uploaded_file.getvalue()}
        try:
            response = requests.post("http://localhost:6000/detect", files=files)
            if response.status_code == 200:
                result = response.json()

                # Show detections
                if "detections" in result:
                    st.subheader("Detected Objects")
                    for det in result["detections"]:
                        st.write(
                            f"**{det['class']}**: "
                            f"Confidence = {det['confidence']}, "
                            f"BBox = {det['bbox']}"
                        )

                # Show output image from base64
                if "output_image_base64" in result:
                    img_bytes = base64.b64decode(result["output_image_base64"])
                    result_img = Image.open(io.BytesIO(img_bytes))
                    st.subheader("Detection Image")
                    st.image(result_img, caption="Detected Objects", use_container_width=True)
                else:
                    st.error("No output image received from AI service.")

            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"Failed to connect to AI service: {e}")
