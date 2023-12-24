# Email Generator GPT

## Description
Email Generator GPT is an interactive web application designed to leverage OpenAI's GPT models for generating customized email responses. Users can input their email-related queries, select the tone and model of their preference, and receive a tailored email response. This application aims to streamline the email drafting process, offering a variety of tones and styles by utilizing the advanced capabilities of GPT-3.5 and other models.
<a href="https://ibb.co/RTYfTGK"><img src="https://i.ibb.co/YBPmB4S/emailgpt.png" alt="emailgpt" border="0"></a>

## Features

- **Custom Email Queries**: Users can input specific scenarios or content they want to include in their emails.
- **Tone Selection**: Offers a variety of tones such as formal, friendly, or assertive to match the user's desired communication style.
- **Model Selection**: Ability to choose from multiple GPT models including the latest GPT-3.5-turbo and others like Davinci and Curie versions.
- **Word Limit Customization**: Users can set the desired length of the email response.
- **Real-time Feedback and Editing**: Users can view, edit, and download the generated email response.
- **Feedback Mechanism**: A built-in feature to collect user feedback to improve the application.
- **Real-time Dashboard**: Visual representation of the usage metrics and popular tones chosen by users.

## Usage

1. **Set Up**: Users start by entering their email query into the text area provided.
2. **Customize**: Select the desired tone, AI model, and word limit for the email response.
3. **Generate**: Click "Generate Email Response" to receive a custom email based on the inputs.
4. **Edit & Download**: Users can edit the generated response and download it as a text file for use.

## Technologies

- **Streamlit**: For creating the web application interface.
- **OpenAI's GPT Models**: The core AI models used for generating email content.
- **Pyrebase**: A simple python interface to Firebase for storing user queries and responses.
- **Requests**: To handle HTTP requests for the feedback form.
- **Plotly**: For creating interactive, real-time dashboards to display usage statistics.

## Installation

To run this project locally, you will need:

- Python 3.6+
- Access to OpenAI API and Firebase.

Install the required Python libraries:

```bash
pip install streamlit openai pyrebase requests plotly
```

## Chrome Plugin in progress
<a href="https://imgbb.com/"><img src="https://i.ibb.co/sj0Z0Lv/image.png" alt="image" border="0"></a>
