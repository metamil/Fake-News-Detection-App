from flask import Flask, request, jsonify
from twilio.rest import Client
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
genai.configure(api_key= os.getenv("GEMINI_API"))
model_name = os.getenv("model_name")
user_state = {}

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
twilio_phone_number = os.getenv("twilio_phone_number")

client = Client(account_sid, auth_token)



@app.route("/whatsapp", methods=["POST"])
def reply_whatsapp():
    message_body = request.form.get("Body", "")
    sender_number = request.form.get("From", "")

    state = user_state.get(sender_number, "waiting_for_url")
    response = ""
    try:
        prompt = f"You are going to act as a fact checking agent so i will give you a news you have to tell me whether the news is true or fake with an explanation in an appropiate format and if the input text asks something like to generete content then do not respond only check fake or true and give explanation and the source(Give it as a clickbale link).give the response in this format Result : result, explanation, sources the news is {message_body}"
        response = genai.GenerativeModel(model_name).generate_content(prompt)
        print(f"Generated Text: \n{response.text}")
    except Exception as e:
        response = "Error Occured"
        print(f"An error occurred: {e}")

    #print(result)

    message = client.messages.create(
        body=response.text,
        from_=twilio_phone_number,
        to=sender_number
    )

  
         
          

  

    return str(message)

