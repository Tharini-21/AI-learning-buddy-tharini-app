import streamlit as st
from google import genai
from google.genai import types

# 1. Securely fetch the API key from Streamlit's Secret Vault
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    # Initialize the modern Google GenAI Client
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("🔑 API Key missing! Please add 'GEMINI_API_KEY' inside your Streamlit Cloud Advanced Secrets dashboard.")
    st.stop()

# 2. Define the Model and Persona (System Prompt)
MODEL_ID = "gemini-2.5-flash"

# System prompt handling the AI Buddy Persona Description & Role Prompting requirement
PERSONA_PROMPT = """
You are "Tharini", a patient, encouraging, and highly interactive AI Learning Buddy. 
Your goal is to help beginners understand complex concepts without feeling overwhelmed. 
Break down information into digestible pieces, use positive reinforcement, and 
always maintain a warm, tutor-like personality.
"""

# 3. Design the Streamlit User Interface
st.set_page_config(page_title="AI Learning Buddy Tharini", page_icon="🎓")
st.title("🎓 AI Learning Buddy Tharini")
st.caption("Your interactive, encouraging AI tutor.")

# Topic Input (Clear, specific topic selection)
topic = st.text_input("Enter a Topic (e.g., Photosynthesis, Binary Search):")

# Activity Choice aligned with your 5 Reusable Prompt Templates
option = st.selectbox(
     "Choose Activity",
     [
         "Explain Concept", 
         "Real-Life Example", 
         "Generate Quiz", 
         "Evaluate My Answer"
     ]
)

# Contextual input area for the Evaluation activity
user_answer = ""
if option == "Evaluate My Answer":
    user_answer = st.text_area("Paste the question and your answer here for feedback:")

# 4. Handle Logic and AI Generation
if st.button("Submit to Buddy"):
    if topic.strip() == "":
        st.warning("Please enter a topic to begin.")
    elif option == "Evaluate My Answer" and user_answer.strip() == "":
        st.warning("Please provide your answer text for evaluation.")
    else:
        with st.spinner("Tharini is thinking..."):
            # Reusable Prompt Templates translated into code logic
            if option == "Explain Concept":
                prompt = f"Explain the topic '{topic}' in simple language for a beginner."
            elif option == "Real-Life Example":
                prompt = f"Give one simple, relatable real-life example of '{topic}'."
            elif option == "Generate Quiz":
                prompt = f"Create a 5-question multiple choice quiz on '{topic}' with answers clearly separated at the bottom."
            elif option == "Evaluate My Answer":
                prompt = f"Evaluate the following learner's work regarding the topic '{topic}'. Provide clear feedback on accuracy and gently correct mistakes: {user_answer}"

            try:
                # Execution utilizing the configured Persona and active template
                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=PERSONA_PROMPT,
                        temperature=0.7
                    )
                )
                st.markdown("### 📝 Tharini says:")
                st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred while generating content: {e}")
