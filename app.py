import streamlit as st
import google.generativeai as genai
import json
import os

# Setup Gemini
st.set_page_config(page_title="NCLEX Socratic Coach", layout="wide")

# Get API Key from Streamlit Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("Please add your GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

st.title("🎓 NCLEX Socratic Prep Dashboard")

# Create tabs for your different Taskade projects
tab1, tab2 = st.tabs(["💬 Chat with Coach", "📊 Study Materials"])

with tab1:
    st.subheader("Socratic Chat")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about Management of Care or Pharmacology..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = model.generate_content(f"You are an NCLEX Socratic Coach. Answer this: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

with tab2:
    st.subheader("Your Taskade Projects")
    # This lists the files you have in your 'projects' folder
    project_files = ["nclex-cognitive-profiler-error-analysis.json", "nclex-master-timeline-apr-28.json"]
    selected_project = st.selectbox("Select a study project to view:", project_files)
    st.info(f"Currently viewing data from: {selected_project}")
    # (Optional: Add logic here to display the JSON content)
