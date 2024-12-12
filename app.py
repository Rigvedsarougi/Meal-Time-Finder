import streamlit as st
from datetime import datetime, timedelta

def calculate_meal_times(wake_up_time, sleep_time, meals_per_day):
    # Parse the input times
    wake_up_time = datetime.strptime(wake_up_time, "%H:%M")
    sleep_time = datetime.strptime(sleep_time, "%H:%M")

    # Calculate the total duration of the day
    if sleep_time < wake_up_time:
        sleep_time += timedelta(days=1)  # Handle overnight sleep times

    total_day = sleep_time - wake_up_time

    # Determine meal intervals
    if meals_per_day == 1:
        intervals = [0.5]  # Single meal in the middle of the day
    elif meals_per_day == 2:
        intervals = [0.25, 0.75]  # Meals at quarter and three-quarters of the day
    elif meals_per_day == 3:
        intervals = [0.2, 0.5, 0.8]  # Breakfast, lunch, and dinner spread evenly
    else:
        raise ValueError("Meals per day must be 1, 2, or 3.")

    # Calculate meal times
    meal_times = [wake_up_time + timedelta(seconds=total_day.total_seconds() * i) for i in intervals]

    # Format the meal times
    meal_names = ["Breakfast", "Lunch", "Dinner"]
    result = {}
    for i, time in enumerate(meal_times):
        result[meal_names[i]] = time.strftime("%H:%M")

    return result

# Streamlit App
st.title("Optimal Meal Time Calculator")

# User Inputs
wake_up_time = st.time_input("Wake-up Time", value=datetime.strptime("07:00", "%H:%M").time())
sleep_time = st.time_input("Sleep Time", value=datetime.strptime("23:00", "%H:%M").time())
meals_per_day = st.selectbox("Number of Meals per Day", options=[1, 2, 3])

# Calculate and Display Meal Times
if st.button("Calculate Meal Times"):
    try:
        wake_up_time_str = wake_up_time.strftime("%H:%M")
        sleep_time_str = sleep_time.strftime("%H:%M")
        meal_schedule = calculate_meal_times(wake_up_time_str, sleep_time_str, meals_per_day)

        st.subheader("Recommended Meal Times:")
        for meal, time in meal_schedule.items():
            st.write(f"{meal}: {time}")
    except Exception as e:
        st.error(f"Error: {e}")
