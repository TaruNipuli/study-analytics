import os.path

import pandas as pd
import streamlit as st

st.title("Study Analytics Dashboard")

st.header("Add study session")

subject = st.text_input("Subject")

hours = st.number_input(
    "Study Hours",
    min_value=0.0,
    max_value=24.0,
    step=0.5
)

difficulty = st.slider(
    "Difficulty",
    min_value=1,
    max_value=5
)

score = st.number_input(
    "Score %",
    min_value=0,
    max_value=100
)

FILE = "study_data.csv"

if st.button("Save"):
    new_data = pd.DataFrame([{
        "subject": subject,
        "hours": hours,
        "difficulty": difficulty,
        "score": score
    }])

    if os.path.exists(FILE):
        old_data = pd.read_csv(FILE)
        data = pd.concat([old_data, new_data], ignore_index=True)
    else:
        data = new_data

    data.to_csv(FILE, index=False)
    st.success("Study session saved!")

st.header("Saved Study Sessions")

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
    st.dataframe(df, hide_index=True)
else:
    st.info("No study sessions saved yet")

