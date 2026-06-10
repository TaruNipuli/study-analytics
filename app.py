import os.path
import pandas as pd
import streamlit as st
from datetime import date
import plotly.express as px

subjects = ["Math", "Physics", "Chemistry", "History", "Biology", "Geography"]

FILE = "study_data.csv"

# reset logic
if "reset" not in st.session_state:
    st.session_state.reset = False

if st.session_state.reset:
    st.session_state.study_date = date.today()
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
if "study_date" not in st.session_state:
    st.session_state.study_date = date.today()

st.title("Study Analytics Dashboard")

st.header("Add study session")

study_date = st.date_input("Study date", key="study_date")

subject = st.selectbox("Subject", subjects, key="subject")

hours = st.number_input("Study Hours", 0.0, 24.0, 0.0, 0.5, key="hours")

difficulty = st.slider("Difficulty", 1, 5, key="difficulty")

#Remove score for now, maybe add later for further analytics
#score = st.number_input("Score %", 0, 100, key="score")

if st.button("Save"):
    new_data = pd.DataFrame([{
        "Date": study_date,
        "Subject": subject,
        "Hours": hours,
        "Difficulty": difficulty,
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

st.header("Study Trends")

if os.path.exists(FILE):
    df = pd.read_csv(FILE)

    # convert date to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # sum hours per subject
    chart_data = df.groupby("Subject", as_index=False)["Hours"].sum()  # groups rows by subject and calculate total hours

    # plotly bar chart
    fig = px.bar(chart_data, x="Subject", y="Hours", title="Total Study Hours per Subject")

    st.plotly_chart(fig, use_container_width=True)

    # sum hours per date
    # group by date, sum hours per day, keep Date as a normal column (not index), and sort by date
    daily_hours = (df.groupby("Date", as_index=False)["Hours"].sum().sort_values("Date"))

    # plotly line chart
    fig = px.line(daily_hours, x="Date", y="Hours", markers=True, title="Study Hours Over Time")

    st.plotly_chart(fig, use_container_width=True)

