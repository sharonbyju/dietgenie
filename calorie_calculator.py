def calculate_daily_calories(current_weight, target_weight, activity_level, age, height, gender):
    # Check for None values and raise an error if any are found
    if current_weight is None or target_weight is None or age is None or height is None:
        raise ValueError("Missing required data: current_weight, target_weight, age, or height cannot be None.")

    # Ensure that current_weight, target_weight, height, and age are valid numbers (not negative or zero)
    if current_weight <= 0 or target_weight <= 0 or age <= 0 or height <= 0:
        raise ValueError("Weight, target weight, age, and height must be positive values.")
    
    # Calculate BMR (Basal Metabolic Rate) based on gender
    if gender == 'Male':
        bmr = 10 * current_weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * current_weight + 6.25 * height - 5 * age - 161

    # Adjust BMR based on activity level
    if activity_level == 'Low':
        daily_calories = bmr * 1.2
    elif activity_level == 'Medium':
        daily_calories = bmr * 1.55
    elif activity_level == 'High':
        daily_calories = bmr * 1.725
    else:
        raise ValueError("Invalid activity level. Choose from 'Low', 'Medium', or 'High'.")

    # Adjust calories for weight loss or gain
    if target_weight < current_weight:
        daily_calories -= 500  # Caloric deficit for weight loss
    elif target_weight > current_weight:
        daily_calories += 500  # Caloric surplus for weight gain

    return daily_calories