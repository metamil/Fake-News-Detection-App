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

    '''if state == "waiting_for_url":
        url = message_body.strip()
        user_state[sender_number] = "processing_url"
        greeting = ["hi", "hello", "hey"]
        if url.lower() in greeting:
            resp = MessagingResponse()
            resp.message("Welcome to ARC")

        elif url.startswith("http"):
            server_url = "http://localhost:5000"
            response = requests.get(f"{server_url}/predict?url={url}")

            score = response.json()['score']

            if score < 50:
                formatted_response = f"The score for {url} is *_{score}_*. This website is safe to use ✅."
            elif score > 50 and score < 70:
                formatted_response = f"The score for {url} is {score}. Please note that this website may be harmful ⚠️."
            elif score > 70:
                formatted_response = f"The score for ~{url}~ is *_{score}_*. Please note that this website is not recommended 🚫."

            message = client.messages.create(
                body=formatted_response,
                from_=twilio_phone_number,
                to=sender_number
            )

        else:
            resp = MessagingResponse()
            resp.message("I can't understand. Drop the link to detect the phishing site.")

            message = client.messages.create(
                body=str(resp),
                from_=twilio_phone_number,
                to=sender_number
            )

        user_state[sender_number] = "waiting_for_url"

    elif state == "processing_url":
        resp = MessagingResponse()
        resp.message("Please wait while we process your URL.")

        message = client.messages.create(
            body=str(resp),
            from_=twilio_phone_number,
            to=sender_number
        )'''

    return str(message)

if __name__ == '__main__':
    app.run()