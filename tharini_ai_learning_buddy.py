import streamlit as st
import google.generativeai as genai

# 1. Fetch the API key from Streamlit's Secret Vault safely
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("🔑 API Key missing! Please add 'GEMINI_API_KEY' inside your Streamlit Cloud Advanced Secrets dashboard.")
    st.stop()

# 2. Set up the Persona (Role Prompting)
# Instruct the AI to act like a patient tutor as required by your guidelines
PERSONA_PROMPT = (
    "You are a patient, encouraging, and highly interactive AI Learning Buddy. "
    "Explain concepts simply, use positive reinforcement, and maintain a warm, tutor-like personality.\n\n"
)

model = genai.GenerativeModel("gemini-2.5-flash")

# 3. Streamlit Interface
st.set_page_config(page_title="AI Learning Buddy Tharini", page_icon="🎓")
st.title("🎓 AI Learning Buddy Tharini")

topic = st.text_input("Enter a Topic")
option = st.selectbox(
    "Choose Activity",
    [
        "Explain Concept",
        "Real-Life Example",
        "Generate Quiz",
        "Evaluate My Answer",  # Required by your assignment guidelines template #4!
        "Ask Anything"
    ]
)

# If evaluating an answer, show a text box to paste the answer
user_answer = ""
if option == "Evaluate My Answer":
    user_answer = st.text_area("Paste the question and your answer here for feedback:")

# 4. Trigger logic
if st.button("Generate"):
    if topic == "":
        st.warning("Please enter a topic.")
    elif option == "Evaluate My Answer" and user_answer == "":
        st.warning("Please provide your answer text for evaluation.")
    else:
        with st.spinner("Thinking..."):
            if option == "Explain Concept":
                prompt = PERSONA_PROMPT + f"Explain {topic} in simple language for a beginner."
            elif option == "Real-Life Example":
                prompt = PERSONA_PROMPT + f"Give one simple real-life example of {topic}."
            elif option == "Generate Quiz":
                prompt = PERSONA_PROMPT + f"Create 5 MCQs on {topic} with answers."
            elif option == "Evaluate My Answer":
                prompt = PERSONA_PROMPT + f"Evaluate this learner's work regarding the topic '{topic}' and give feedback: {user_answer}"
            else:
                prompt = PERSONA_PROMPT + topic

            response = model.generate_content(prompt)
            st.write(response.text)
