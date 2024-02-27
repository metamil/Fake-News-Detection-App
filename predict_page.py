import streamlit as st
import requests
import json

def detect(text):
   url = "https://tamilselvanm.us-east-1.modelbit.com/v1/predict_news/3"
   body = {'data': text}
   x =  requests.post(url, json=body)
   return json.loads(x.text)


def show_page():
    st.title("Fake News Detector")
    input  = st.text_input(label = "Enter the News")
    click = st.button("Detect")

    if click:
        res = detect(input)
        if(res["data"][0][0]==0):
         st.subheader("Fake news Detected")
        else:
            st.subheader("No Fake news Detected")
show_page()

