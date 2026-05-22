import pandas as pd
import os

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


df = pd.DataFrame({"calories": [1,2,3,4,5], "height": [1,2,1,2,2]})
save(df,'workout-tracker/workouts.csv')
