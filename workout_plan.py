def generate_workout_plan(activity_level):
    workout_plan = {}
    if activity_level == 'Low':
        workout_plan = {
            'workouts': ['Walking for 30 minutes', 'Stretching for 15 minutes', 'Yoga for 30 minutes', 'Light Swimming for 20 minutes']
        }
    elif activity_level == 'Medium':
        workout_plan = {
            'workouts': ['Jogging for 30 minutes', 'Yoga for 45 minutes', 'Cycling for 30 minutes', 'HIIT for 20 minutes']
        }
    elif activity_level == 'High':
        workout_plan = {
            'workouts': ['Running for 45 minutes', 'Weight Training (1 hour)', 'HIIT for 30 minutes', 'CrossFit for 45 minutes']
        }
    return workout_plan