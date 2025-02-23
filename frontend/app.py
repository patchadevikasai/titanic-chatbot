import streamlit as st
import requests
from PIL import Image
import base64
from io import BytesIO

API_URL = "http://127.0.0.1:8000"

st.title("🚢 Titanic Dataset Chatbot")

user_query = st.text_input("Ask about the Titanic dataset:")

if st.button("Ask"):
    if user_query:
        response = requests.get(f"{API_URL}/query/", params={"question": user_query}).json()
        st.write("🤖 Bot:", response["answer"])
        
        if any(word in user_query.lower() for word in ["histogram", "show me", "plot"]):
            vis_response = requests.get(f"{API_URL}/visualize/", params={"query": user_query}).json()
            if "image" in vis_response:
                image_data = base64.b64decode(vis_response["image"])
                image = Image.open(BytesIO(image_data))
                st.image(image, caption="Generated Visualization")
