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
