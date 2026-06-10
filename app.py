import os.path
import pandas as pd
import streamlit as st

subjects = ["Math", "Physics", "Chemistry", "History", "Biology", "Geography"]

FILE = "study_data.csv"

# reset logic
if "reset" not in st.session_state:
    st.session_state.reset = False

if st.session_state.reset:
    st.session_state.subject = subjects[0]
    st.session_state.hours = 0.0
    st.session_state.difficulty = 1
    st.session_state.score = 0
    st.session_state.reset = False

# default values
if "subject" not in st.session_state:
    st.session_state.subject = subjects[0]
if "hours" not in st.session_state:
    st.session_state.hours = 0.0
if "difficulty" not in st.session_state:
    st.session_state.difficulty = 1
if "score" not in st.session_state:
    st.session_state.score = 0

st.title("Study Analytics Dashboard")

st.header("Add study session")

subject = st.selectbox("Subject", subjects, key="subject")

hours = st.number_input("Study Hours", 0.0, 24.0, 0.0, 0.5, key="hours")

difficulty = st.slider("Difficulty", 1, 5, key="difficulty")

score = st.number_input("Score %", 0, 100, key="score")

if st.button("Save"):
    new_data = pd.DataFrame([{
        "Subject": subject,
        "Hours": hours,
        "Difficulty": difficulty,
        "Score %": score
    }])

    if os.path.exists(FILE):
        old_data = pd.read_csv(FILE)
        data = pd.concat([old_data, new_data], ignore_index=True)
    else:
        data = new_data

    data.to_csv(FILE, index=False)

    st.success("Saved!")

    # trigger reset next rerun
    st.session_state.reset = True
    st.rerun()

st.header("Saved Study Sessions")

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
    st.dataframe(df, hide_index=True)