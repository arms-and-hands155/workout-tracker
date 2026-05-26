import pandas as pd
import os
import streamlit as st
from datetime import date
from pathlib import Path

script_path = Path(__file__).resolve()
project_root = script_path.parent
file_location = project_root / "workouts.csv"


def load(file):
    if not file.exists():
        return pd.DataFrame(columns=["Date", "Day type", "Exercise", "Set column", "Reps", "Weight", "Completed"])
    try:
        return pd.read_csv(file, parse_dates=["Date"])
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["Date", "Day type", "Exercise", "Set column", "Reps", "Weight", "Completed"])

def save(workout, file): #Save and update file
    try:
        if(os.path.isfile(file)) and os.path.getsize(file): #If file exists and isn't empty
            workout.to_csv(file, mode ='a', header=False, index=False) #Don't add the header
        else:
            workout.to_csv(file, mode ='a',  index=False)
    except OSError:
        return

def recent_day(type): #Get the most recent workout of type selected
    smt_df = df[df['Day type'] == type]
    recent_date = smt_df['Date'].max()
    smt_df = smt_df.drop('Day type', axis=1)

    return smt_df[smt_df['Date'] == recent_date]

def overload(exercise_df):
    if not exercise_df.empty and exercise_df['Completed'].all():
        return 5
    return 0

df = load(file_location)
st.title("🏋️‍♂️ Workout Tracker")

select = st.selectbox( #Picking a workout type
    "Workout Type",
    ["Push", "Pull", "Legs", "Upper", "Lower"],
    index=None,
    placeholder="Select a Workout template",
    accept_new_options=True,
)

if select is not None:
    Data = {"Date":[], "Day type":[], "Exercise":[], "Set number":[], "Reps":[], "Weight":[], "Completed":[] }
    check = recent_day(select)
    st.write(f"Last {select} day: ", check if not check.empty else "No data provided")

    if "set_counts" not in st.session_state or st.session_state.get('current_day') != select:
        st.session_state.set_counts = {}
        st.session_state.current_day = select

        if not check.empty:
            for e in check['Exercise'].unique():
                prev_set_count = len(check[check['Exercise']==e])
                st.session_state.set_counts[e] = prev_set_count
        else:
            st.session_state.set_counts = {}

    data = []
    
    if not check.empty:
        for e in check['Exercise'].unique():
            check_exercise = check[check['Exercise'] == e]
            bonus = overload(check_exercise)

            st.subheader(e, divider="red")
            current_sets = st.session_state.set_counts.get(e,1)

            for j in range(current_sets):
                if j<len(check_exercise):
                    prev_reps = int(check_exercise.iloc[j]['Reps'])
                    prev_weight = int(check_exercise.iloc[j]['Weight']) 
                else:
                    prev_reps = 0
                    prev_weight = int(check_exercise.iloc[-1]['Weight']) if not check_exercise.empty else 0

                st.write(f"Set {j+1}")
                col1,col2,col3 = st.columns(3)

                with col1:
                    reps = st.number_input("Reps", value=prev_reps, key=f"reps_{e}_{j}")
                with col2:
                    suggested_w = prev_weight + (bonus if j < len(check_exercise) else 0)
                    weight = st.number_input("Weight", value=suggested_w, key=f"weight_{e}_{j}")
                with col3:
                    complete = st.checkbox("Done", key=f"Complete_{e}_{j}")
                
                data.append({
                    "Date": date.today(),
                    "Day type": select,
                    "Exercise": e,
                    "Set number": j+1,
                    "Reps": reps,
                    "Weight": weight,
                    "Completed": complete
                })

            btn_col1, btn_col2 = st.columns(2)
            if btn_col1.button(f"➕ Add Set to {e}", key=f"add_{e}"):
                st.session_state.set_counts[e] += 1
                st.rerun()
            if btn_col2.button(f"➖ Remove Set from {e}", key=f"rem_{e}"):
                if st.session_state.set_counts[e] > 1:
                    st.session_state.set_counts[e] -= 1
                    st.rerun()

        st.divider()
        if st.button("Log Workout", type="primary"): #Logging workout
            if data:
                dataframe = pd.DataFrame(data)
                save(dataframe, file_location)
                st.success("Workout logged successfully!")
            else:
                st.warning("No data to save.")
    else:
        st.write("No data provided")




        