import streamlit as st
from groq import Groq
import toml
import subprocess
import tempfile
import os

# Load config
@st.cache_resource
def load_config():
    return toml.load("config/config.toml")

config = load_config()
llms = config.get("llm", [])

# Initialize client
client = Groq(api_key=llms[0]["api_key"])

# Code execution function
def run_code(code: str) -> str:
    """Run Python code in a secure temporary environment"""
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, "script.py")
            with open(script_path, "w") as f:
                f.write(code)
            result = subprocess.run(
                ["python", script_path],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=tmpdir
            )
            return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Code took too long to execute (max 5s)."
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="OpenManus Pro", layout="wide", page_icon="🧠")
st.title("🧠 OpenManus Pro – AI Research Assistant")

# Sidebar
with st.sidebar:
    st.header("🧠 Model Settings")
    selected_model = st.selectbox("Select LLM", options=[m["name"] for m in llms])
    st.markdown("---")
    st.markdown("📄 Ask anything below — or use the code runner!")

# Main chat area
prompt = st.text_area("📝 Enter your question:", height=200, placeholder="Ask about science, coding, research...")

if st.button("🧠 Generate Response"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=llms[0]["model"],
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown("### 💬 Response:")
                st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")

# Code runner section
with st.expander("🔧 Run Python Code"):
    code_prompt = st.text_area("Enter Python code:", height=200)
    if st.button("▶️ Execute Code"):
        with st.spinner("Running code..."):
            output = run_code(code_prompt)
            st.code(output, language="bash")
            
