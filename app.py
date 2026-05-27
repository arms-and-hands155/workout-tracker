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
        df = pd.read_csv(file, parse_dates=["Date"], on_bad_lines='warn') #skip over any potential broken lines
        if not df.empty:
            df['Date'] = df['Date'].dt.date 
        return df
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["Date", "Day type", "Exercise", "Set column", "Reps", "Weight", "Completed"])
    except Exception as e:
        return pd.DataFrame(columns=["Date", "Day type", "Exercise", "Set column", "Reps", "Weight", "Completed"])

def save(workout, file):
    try:
        if(os.path.isfile(file)) and os.path.getsize(file):
            with open(file, 'rb+') as f:
                f.seek(-1, os.SEEK_END)
                if f.read(1) != b'\n':
                    f.write(b'\n')
            workout.to_csv(file, mode='a', header=False, index=False, lineterminator='\n')
        else:
            workout.to_csv(file, mode='w', index=False, lineterminator='\n')
    except OSError as e:
        st.error(f"Error saving file: {e}")

def recent_day(type):
    smt_df = df[df['Day type'] == type]
    if smt_df.empty:
        return pd.DataFrame()
    recent_date = smt_df['Date'].max()
    smt_df = smt_df[smt_df['Date'] == recent_date]
    return smt_df.drop('Day type', axis=1)

def overload(exercise_df):
    if not exercise_df.empty and exercise_df['Completed'].all():
        return 5
    return 0

df = load(file_location)
st.title("🏋️‍♂️ Workout Tracker")

# History display
if "show_history" not in st.session_state:
    st.session_state.show_history = False

if st.button("View History"):
    st.session_state.show_history = not st.session_state.show_history

if st.session_state.show_history:
    filter_choice = st.radio("Filter History By:", ["None", "Day type", "Exercise"], horizontal=True)
    history_df = df.copy()

    if filter_choice == "Day type":
        day_filter = st.selectbox("Select Workout Type", ["Push", "Pull", "Legs", "Upper", "Lower"], index=None)
        if day_filter:
            history_df = history_df[history_df['Day type'] == day_filter]
    elif filter_choice == "Exercise":
        unique_ex = df['Exercise'].unique().tolist()
        ex_filter = st.selectbox("Select Exercise", unique_ex, index=None)
        if ex_filter:
            history_df = history_df[history_df['Exercise'] == ex_filter]

    history_df = history_df.sort_values(by="Date", ascending=False)
    st.dataframe(history_df, use_container_width=True, hide_index=True)

st.divider()

select = st.selectbox(
    "Workout Type",
    ["Push", "Pull", "Legs", "Upper", "Lower"],
    index=None,
    placeholder="Select a Workout template",
)

if select is not None:
    check = recent_day(select)
    
    if "current_day" not in st.session_state or st.session_state.current_day != select:
        st.session_state.current_day = select
        st.session_state.extra_exercises = []
        st.session_state.set_counts = {}
        
        if not check.empty:
            for e in check['Exercise'].unique():
                st.session_state.set_counts[e] = len(check[check['Exercise'] == e])

    data = []
    
    # Master exercise list
    history_exercises = list(check['Exercise'].unique()) if not check.empty else []
    all_current_exercises = history_exercises + st.session_state.extra_exercises

    # Main Loop for Exercises
    for e in all_current_exercises:
        check_exercise = check[check['Exercise'] == e] if not check.empty else pd.DataFrame()
        bonus = overload(check_exercise)
        
        st.subheader(e, divider="red")
        current_sets = st.session_state.set_counts.get(e, 1)

        for j in range(current_sets):
            if not check_exercise.empty and j < len(check_exercise):
                prev_reps = int(check_exercise.iloc[j]['Reps'])
                prev_weight = int(check_exercise.iloc[j]['Weight'])
            else:
                prev_reps = 0
                prev_weight = int(check_exercise.iloc[-1]['Weight']) if not check_exercise.empty else 0

            st.write(f"**Set {j+1}**")
            col1, col2, col3 = st.columns(3)

            with col1:
                reps = st.number_input("Reps", value=prev_reps, key=f"reps_{e}_{j}")
            with col2:
                applied_bonus = bonus if (not check_exercise.empty and j < len(check_exercise)) else 0
                weight = st.number_input("Weight", value=prev_weight + applied_bonus, key=f"weight_{e}_{j}")
            with col3:
                complete = st.checkbox("Done", key=f"Complete_{e}_{j}")
            
            data.append({
                "Date": date.today(),
                "Day type": select,
                "Exercise": e,
                "Set column": j+1,
                "Reps": reps,
                "Weight": weight,
                "Completed": complete
            })

        # Set modification buttons per exercise
        btn_col1, btn_col2 = st.columns(2)
        if btn_col1.button(f"➕ Add Set to {e}", key=f"add_{e}"):
            st.session_state.set_counts[e] = st.session_state.set_counts.get(e, 1) + 1
            st.rerun()
        if btn_col2.button(f"➖ Remove Set from {e}", key=f"rem_{e}"):
            if st.session_state.set_counts.get(e, 1) > 1:
                st.session_state.set_counts[e] -= 1
                st.rerun()

    st.divider()
    st.write("Add Exercuse")
    new_ex_name = st.text_input("Exercise Name", placeholder="e.g. Incline Bench", key="new_ex_input")
    
    if st.button("➕ Add New Exercise"):
        if new_ex_name and new_ex_name not in all_current_exercises:
            st.session_state.extra_exercises.append(new_ex_name)
            st.session_state.set_counts[new_ex_name] = 1
            st.rerun()
        else:
            st.warning("Invalid name or exercise already exists.")

    if st.button("Log Workout", type="primary"):
        if data:
            save(pd.DataFrame(data), file_location)
            st.success("Workout logged successfully!")
        else:
            st.warning("No data to save.")