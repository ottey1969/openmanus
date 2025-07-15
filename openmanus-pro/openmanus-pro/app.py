import streamlit as st
from groq import Groq
import os

# Load API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# Streamlit UI
st.set_page_config(page_title="OpenManus Pro", layout="wide", page_icon="🧠")
st.title("🧠 OpenManus Pro – AI Research Assistant")

prompt = st.text_area("📝 Enter your question:", height=200)
if st.button("Generate Response"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Thinking..."):
            try:
                client = Groq(api_key=groq_api_key)
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown("### 💬 Response:")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")