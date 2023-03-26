import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_email(prompt, tone, model_engine, word_limit):
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

    return response.choices[0].text.strip()

st.title("Email Response Generator")

email_query = st.text_area("Enter your email query:", value="", height=150)
tone = st.selectbox("Select the tone of the email response:", ["Formal", "Friendly", "Neutral"])
model_engine = st.selectbox("Select the AI model:", [
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
    else:
        prompt = f"Generate an email response to the following query in a {tone.lower()} tone:\n\n{email_query}\n\nResponse:"
        email_response = generate_email(prompt, tone, model_engine, word_limit)
        st.markdown(f"**Generated Email Response ({tone} Tone) using {model_engine}:**")
        st.write(email_response)
