import streamlit as st

from mock_interview import mi
from ai_tutor import tutor
from ats_analyzer import ats

st.set_page_config(page_title="Ai learning partner", layout ="wide")
st.title("AI LEARNING PARTNER")

mode=st.sidebar.radio(
    "select mode",
    ["Mock Interview","AI Tutor","ATS Analyzer"]
)

if mode=="Mock Interview":
    st.subheader("Mock Interview Mode")
    mock_interview()

elif mode=="AT Tutor":
    st.subheader("AI Tutor Mode")
    ai_tutor()

elif mode=="ATS Analyzer":
    st.subheader("ATS Resume Analyzer Mode")
    ats()        