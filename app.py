import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="QuizTube",
    page_icon="🧠",
    layout="centered"
)

def clicked(button):
    with st.sidebar:
        if not nickname:
            st.error("Please set a nickname.")
        elif not language:
            st.error("Please select language.")
        elif not topic:
            st.error("Please select a topic.")
        elif not difficulty_level:
            st.error("Please select a difficulty level.")
        else:
            disable()
            st.session_state.clicked[button] = True

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Check if user is new or returning using session state.
# If user is new, show the toast message.
if 'first_time' not in st.session_state:
    st.session_state.first_time = False

# Initialize the key in session state
if 'clicked' not in st.session_state:
    st.session_state.clicked = {1:False}

# Disable the submit button after it is clicked
def disable():
    st.session_state.disabled = True

# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False

with st.sidebar:
    st.header("Player's Profile")

    nickname = st.text_input("Enter a nickname", type="default", disabled=st.session_state.disabled)
    #openai_api_key = st.text_input("Enter API Key", type="password")

    st.divider()
    language = st.selectbox(
        'Choose the language',
        ('English', 'Japanese'),
        None,
        disabled=st.session_state.disabled
    )

    st.divider()
    topic = st.selectbox(
        'Choose the topic',
        ('AWS', 'Azure', 'JLPT', 'IELTS'),
        None,
        disabled=st.session_state.disabled
    )

    st.divider()
    difficulty_level = st.radio(
        "Choose the difficulty level",
        ("Easy", "Normal", "Hard"),
        None,
        disabled=st.session_state.disabled
    )

    st.button("Ready!", type="primary", on_click=clicked, args=[1], disabled=st.session_state.disabled)

# Chat UI title
st.title(":red[Take a Guess!] — Think. Guess. Fight!", anchor=False)
st.subheader('Stop the aliens by guessing the correct answer before the bomb explodes!')

with st.expander("💡 Video Tutorial"):
    with st.spinner("Loading video.."):
        st.video("https://youtu.be/yzBr3L2BIto", format="video/mp4", start_time=0)

if st.session_state.clicked[1]:
    st.write(nickname)
    st.write(language)
    st.write(topic)
    st.write(difficulty_level)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})