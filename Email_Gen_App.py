import streamlit as st
import openai
import time

openai.api_key = st.secrets["OPENAI_API_KEY"]


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


def generate_email(prompt, tone, model_engine, word_limit):
    # Create a progress bar placeholder
    progress_bar = st.progress(0)


    # Simulate progress (replace this with actual progress updates if possible)
    for i in range(50):
        time.sleep(0.1)
        progress_bar.progress((i + 1) / 10)


    if model_engine == 'gpt-3.5-turbo':
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages = [{"role":"user","content":prompt}]
        )
        progress_bar.progress(1)
        return response.choices[0].message.content.strip()
    else:

        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=word_limit,
            n=1,
            stop=None,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Set progress bar to 100%
        progress_bar.progress(1)

        return response.choices[0].text.strip()

st.title("Email Response Generator")

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
        st.write(email_response)