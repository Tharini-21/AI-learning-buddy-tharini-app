import streamlit as st
import google.generativeai as genai

# 1. Securely fetch the API key from Streamlit's Secret Vault
# Make sure you add GEMINI_API_KEY to your Advanced Settings -> Secrets on Streamlit Cloud!
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("🔑 API Key missing! Please add 'GEMINI_API_KEY' inside your Streamlit Cloud Advanced Secrets dashboard.")
    st.stop()

# 2. Initialize the Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")

# 3. Design the Streamlit User Interface
st.set_page_config(page_title="AI Learning Buddy Tharini", page_icon="🎓")
st.title("🎓 AI Learning Buddy Tharini")

topic = st.text_input("Enter a Topic")
option = st.selectbox(
     "Choose Activity",
     ["Explain Concept", "Real-Life Example", "Generate Quiz", "Ask Anything"]
)

# 4. Handle Logic and AI Generation
if st.button("Generate"):
    if topic.strip() == "":
        st.warning("Please enter a topic.")
    else:
        # Show a loading spinner while the AI works
        with st.spinner("Thinking..."):
            if option == "Explain Concept":
                prompt = f"Explain {topic} in simple language for a beginner."
            elif option == "Real-Life Example":
                prompt = f"Give one simple real-life example of {topic}."
            elif option == "Generate Quiz":
                prompt = f"Create 5 MCQs on {topic} with answers."
            else:
                prompt = topic

            try:
                response = model.generate_content(prompt)
                st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred while generating content: {e}")
