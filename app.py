import pandas as pd
import os
import streamlit as st

def load(file):
    try:
        workouts = pd.read_csv(file)
        return workouts
    except pd.errors.EmptyDataError:
        return pd.DataFrame({"Date":[], "Day type":[], "Exercise":[], "Set number":[], "Reps":[], "Weight":[], "Completed":[] })

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
    smt_df =smt_df.drop('Day type', axis=1)

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

    for i,e in enumerate(check['Exercise'].unique()):
        check_exercise = check[check['Exercise'] == e]
        count = len(check_exercise)

        st.subheader(e, divider=True)

        for j in range(count):
            Reps = st.number_input(
                "Enter Reps", 
                min_value= check_exercise.iloc[j,3],
                key = (f"reps_{e}_{j}")
            )
            Weight = st.number_input(
                "Enter Weight", 
                min_value= check_exercise.iloc[j,4],
                key = (f"weight_{e}_{j}")
            )

            Complete = st.checkbox(
                "Completed",
                key=(f"Complete_{e}_{j}")
            )
