import pandas as pd
import os
import streamlit as st

def load(file):
    try:
        workouts = pd.read_csv(file)
        return workouts
    except pd.errors.EmptyDataError:
        return pd.DataFrame({"Date":[], "Day type":[], "Exercise":[], "Sets":[], "reps":[], "Weight":[], "Completed":[] })

def save(workout, file):
    try:
        x=load(file)
        if(os.path.isfile(file)) and not x.empty:
            workout.to_csv(file, mode ='a', header=False, index=False)
        else:
            workout.to_csv(file, mode ='a',  index=False)
    except OSError:
        return

def recent_day(type):
    smt_df = df[df['Day type'] == type]
    recent_date = smt_df['Date'].max()

    return smt_df[smt_df['Date'] == recent_date]

df= load('/Users/armand_k/Workout app/workout-tracker/workouts.csv')

select = st.selectbox(
    "Workout Type",
    ["Push", "Pull", "Legs", "Upper", "Lower"],
    index=None,
    placeholder="Select a Workout template",
    accept_new_options=True,
)
if select is not None:
    check = recent_day(select)
    st.write(f"Last {select} day: ", check if not check.empty else "No data provided")

