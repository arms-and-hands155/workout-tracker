# Workout Tracker

A lightweight Streamlit app for logging gym workouts, tracking progressive overload, and visualizing exercise progress over time.

## Features

- **Workout Templates** — Choose from Push, Pull, Legs, Upper, Lower, or add your own day type
- **Smart Pre-filling** — Automatically loads your last session's sets, reps, and weights so you always have a starting point
- **Progressive Overload** — Adds 5 lbs to exercises where you completed every set in your previous session
- **Flexible Set Management** — Add or remove sets per exercise on the fly
- **Custom Exercises** — Add any exercise to your session beyond the template defaults
- **Delete Exercises** — Remove any exercise from a session before logging
- **Workout History** — Browse all past sessions, filterable by workout type or exercise
- **Progress Charts** — Line chart showing max weight over time for any exercise

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/your-username/workout-tracker.git
cd workout-tracker
pip install streamlit pandas
```

### Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## How It Works

### Logging a Workout

1. Select a workout type from the dropdown (Push, Pull, Legs, Upper, Lower)
2. Your most recent session of that type is loaded as a template
3. Adjust reps and weights for each set — or add/remove sets as needed
4. Add any extra exercises using the text input at the bottom
5. Check the **Done** checkbox for each completed set
6. Click **Log Workout** to save

### Progressive Overload

If every set in an exercise was marked as completed in your last session, the app automatically adds **5 lbs** to the suggested weight for that exercise. This encourages consistent progression.

### Viewing History

Click **View History** to expand the history panel. You can filter by:
- **Day type** — e.g. all Push days
- **Exercise** — e.g. all Bench Press entries

### Tracking Progress

Click **View Workout Progression**, select an exercise, and see a line chart of your max weight over time.

## Data Storage

Workouts are saved locally to a `workouts.csv` file in the same directory as the script. The file is created automatically on first use.

| Column | Description |
|--------|-------------|
| `Date` | Date the workout was logged |
| `Day type` | Workout template used (Push, Pull, etc.) |
| `Exercise` | Exercise name |
| `Set column` | Set number within the exercise |
| `Reps` | Reps performed |
| `Weight` | Weight used |
| `Completed` | Whether the set was marked done |

## Project Structure

```
workout-tracker/
├── app.py           # Main Streamlit app
├── workouts.csv     
└── README.md
```
