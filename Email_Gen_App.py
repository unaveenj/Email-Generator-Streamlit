import streamlit as st
import openai
import requests
import pyrebase
from datetime import datetime
import pytz

st.image("Logo.png",use_column_width=True)

# set the timezone to Asia/Singapore
sg_timezone = pytz.timezone('Asia/Singapore')

# get the current date and time in Singapore timezone
now = datetime.now(sg_timezone)

# format the date as dd-mm-yy
formatted_datetime = now.strftime('%d-%m-%y %H:%M:%S')

FORMSPREE_ENDPOINT = "https://formspree.io/f/mqkoydrl"


openai.api_key = st.secrets["OPENAI_API_KEY"]

config = {
    "apiKey": st.secrets["FIREBASE_API"],
    "authDomain": st.secrets["AUTH_DOMAIN"],
    "databaseURL": st.secrets["DATABASE"],
    "projectId": st.secrets["PROJECT_ID"],
    "storageBucket": st.secrets["STORAGE_BUCKET"],
    "messagingSenderId": st.secrets["SENDER_ID"],
    "appId": st.secrets["APP_ID"],
    "measurementId": st.secrets["MEASUREMENT_ID"]
}

firebase = pyrebase.initialize_app(config=config)

database = firebase.database()


def send_formspree_feedback(user_email, feedback):
    data = {
        "user_email": user_email,
        "feedback": feedback
    }
    response = requests.post(FORMSPREE_ENDPOINT, data=data)

    if response.status_code == 200:
        st.success("Feedback sent successfully!")
    else:
        st.error("An error occurred while sending the feedback. Please try again.")


def is_email_related(query):
    keywords = [
        "email",
        "subject",
        "recipient",
        "cc",
        "bcc",
        "body",
        "attachment",
        "compose",
        "draft",
        "reply",
        "forward",
        "signature",
        "write",
        "send",
        "mail",
        "compose"
    ]
    query_words = query.lower().split()
    return any(keyword in query_words for keyword in keywords)

def generate_email(prompt, tone,model_engine,word_limit):
    if model_engine == 'gpt-3.5-turbo':
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages = [{"role":"user","content":prompt}]
        )
        return response.choices[0].message.content.strip()

    else:
        # model_engine = "text-davinci-002"  # You can use other models like "text-curie-002", "text-babbage-002", etc.
        response = openai.ChatCompletion.create(
            model=model_engine,
            prompt=prompt,
            max_tokens=word_limit,
            n=1,
            stop=None,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].text.strip()


email_query = st.text_area("Enter your email query:", value="", height=150)
tone = st.selectbox("Select the tone of the email response:", [
    "Formal",
    "Friendly",
    "Neutral",
    "Polite",
    "Casual",
    "Enthusiastic",
    "Diplomatic",
    "Humorous",
    "Assertive",
    "Apologetic",
    "Encouraging",
    "Grateful",
    "Serious",
    "Unapologetic"
])
model_engine = st.selectbox("Select the AI model:", [
    'gpt-3.5-turbo',
    "text-davinci-003",
    "text-davinci-002",
    "text-curie-002",
    "text-babbage-002",
    "text-ada-002"
])
word_limit = st.number_input("Select the number of words for the response:", min_value=50, max_value=500, value=100, step=50)

if st.button("Generate Email Response"):
    with st.spinner("Generating response..."):
        if not email_query:
            st.warning("Please enter an email query to generate a response.")
        elif not is_email_related(email_query):
            st.warning("Please enter a query related to creating emails.")
        else:
            prompt = f"""
        You are an AI language model assisting in generating email responses. Your assistant mode is set to '{tone.lower()}' tone.
    
        User: {email_query}
    
        AI:"""
            email_response = generate_email(prompt, tone, model_engine, word_limit)
            st.markdown(f"**Generated Email Response ({tone} Tone) using {model_engine}:**")
            edited_email = st.text_area("Edit the generated email response (if needed):", value=email_response, height=500)

            if st.download_button("Download Email Response as Text File", data=edited_email.encode("utf-8"),
                                  file_name="email_response.txt", mime="text/plain"):
                st.success("Email response downloaded successfully.")

        data = {"Prompt":email_query , "Tone":tone , "Output":email_response}
        database.child(f"{formatted_datetime}").set(data)

st.markdown("### Feedback")
user_email = st.text_input("Your email:")
feedback = st.text_area("We'd love to hear your feedback! Share your thoughts here:")
if st.button("Send Feedback"):
    if not user_email:
        st.warning("Please enter your email address.")
    elif not feedback:
        st.warning("Please enter your feedback.")
    else:
        send_formspree_feedback(user_email, feedback)

st.markdown("### Source Code")
st.markdown("[GitHub Repository](https://github.com/unaveenj/Email-Generator-Streamlit)")
