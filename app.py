import streamlit as st
import pandas as pd
from datetime import date
import os

CSV_FILE = "workouts.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["date", "day_type", "exercise", "sets", "reps", "weight", "completed"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

def suggest_weight(df, exercise, current_weight, completed):
    if completed:
        return current_weight + 5
    return current_weight

st.title("Workout Tracker")

df = load_data()

day_type = st.selectbox("Today's workout", ["Push", "Pull", "Legs", "Upper", "Lower"])
exercise = st.text_input("Exercise name")
sets = st.number_input("Sets", min_value=1, max_value=10, value=3)
reps = st.number_input("Reps", min_value=1, max_value=30, value=8)
weight = st.number_input("Weight (lbs)", min_value=0, max_value=1000, value=0)
completed = st.checkbox("Completed all sets and reps?")

if st.button("Log workout"):
    new_row = {
        "date": date.today(),
        "day_type": day_type,
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
        "weight": weight,
        "completed": completed
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    suggestion = suggest_weight(df, exercise, weight, completed)
    st.success(f"Logged! Next session try {suggestion}lbs")

st.subheader("Your logs")
st.dataframe(df)