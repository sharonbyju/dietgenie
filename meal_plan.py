def generate_plan(dietary_preference, activity_level):
    #plan = {}

    # Define meal plans based on dietary preference
    if dietary_preference == 'Vegan':
        meal_plan = {
            'breakfast': ['Vegan Smoothie Bowl', 'Chia Pudding'],
            'lunch': ['Vegan Buddha Bowl', 'Quinoa Salad'],
            'dinner': ['Vegan Chili', 'Tofu Stir-Fry'],
            'snack': ['Apple with Peanut Butter', 'Roasted Chickpeas']
        }
    elif dietary_preference == 'Veg':
        meal_plan = {
            'breakfast': ['Vegetable Poha', 'Avocado Toast'],
            'lunch': ['Chickpea Curry', 'Lentil Soup'],
            'dinner': ['Paneer Butter Masala', 'Vegetable Biryani'],
            'snack': ['Fruit Salad', 'Mixed Nuts']
        }
    else:  # Non-Veg
        meal_plan = {
            'breakfast': ['Egg Omelette', 'Greek Yogurt'],
            'lunch': ['Grilled Chicken Salad', 'Chicken Stir-Fry'],
            'dinner': ['Grilled Salmon', 'Baked Chicken Breast'],
            'snack': ['Boiled Eggs', 'Chicken Skewers']
        }

    # Adjust workout plan based on activity level
    if activity_level == 'Low':
        workouts = ['Walking', 'Stretching']
    elif activity_level == 'Medium':
        workouts = ['Jogging', 'Yoga']
    else:
        workouts = ['Running', 'Weight Training']

    # Storing both plans in the dictionary
    plan['meal_plan'] = meal_plan
    plan['workout_plan'] = workouts

    #return plan

    return {
            'meals': meals,
            'workout_plan': workout_plan
        }