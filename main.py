import streamlit as st

from backend.mock_interview import mock_interview
from backend.ai_tutor import ai_tutor
from backend.ats_analyzer import ats

st.set_page_config(page_title="Ai learning partner", layout ="wide")
st.title("AI LEARNING PARTNER")

mode=st.sidebar.radio(
    "select mode",
    ["Mock Interview","AI Tutor","ATS Analyzer"]
)

if mode=="Mock Interview":
    st.subheader("Mock Interview Mode")
    mock_interview()

elif mode=="AI Tutor":
    st.subheader("AI Tutor Mode")
    ai_tutor()

elif mode=="ATS Analyzer":
    st.subheader("ATS Resume Analyzer Mode")
    ats()        