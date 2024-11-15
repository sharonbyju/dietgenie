from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from models import db, User  # Import the db and User model from models.py
from meal_plan import generate_plan
from workout_plan import generate_workout_plan
from calorie_calculator import calculate_daily_calories

# Initialize Flask app
app = Flask(__name__)

# Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Database URI (use your desired database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Set a secret key for sessions

# Initialize the database
db.init_app(app)  # Initialize db with the app
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Fetch user by ID

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Use .get() to avoid KeyError if 'dietary_preference' is missing
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        dietary_preference = request.form.get('dietary_preference')
        activity_level = request.form.get('activity_level')

        if not dietary_preference or not activity_level:
            # Handle the case where dietary preference or activity level is missing
            return "Dietary preference and activity level are required!", 400

        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # Return an error message if the email is already in use
            return "Email address already in use. Please choose another one.", 400

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user object and save it to the database
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            dietary_preference=dietary_preference,
            activity_level=activity_level
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  # Redirect to login page after registration

    return render_template('register.html')  # Render the registration form on GET request

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')

        if not username_or_email or not password:
            return "Username/Email and password are required!", 400

        # Strip any whitespace from the input
        username_or_email = username_or_email.strip()

        # Try to find the user by email first
        user = User.query.filter_by(email=username_or_email).first()

        # If user not found by email, try by username
        if not user:
            user = User.query.filter_by(username=username_or_email).first()

        if user:
            # Check if the password matches the stored hash
            if check_password_hash(user.password_hash, password):
                login_user(user)  # Log the user in
                return redirect(url_for('dashboard'))  # Redirect to the dashboard
            else:
                return "Incorrect password!", 401
        else:
            return "Invalid email or password!", 401

    return render_template('login.html')  # Render the login form on GET request

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Profile route
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Process profile update logic here
        username = request.form['username']
        email = request.form['email']
        dietary_preference = request.form['dietary_preference']
        activity_level = request.form['activity_level']
        current_weight = request.form['current_weight']
        goal = request.form['goal']

        # Assuming 'user' is the logged-in user object, update their profile
        user = current_user  # Get the logged-in user
        
        user.username = username
        user.email = email
        user.dietary_preference = dietary_preference
        user.activity_level = activity_level
        user.current_weight = current_weight
        user.goal = goal

        # Commit the changes to the database
        db.session.commit()
        
        flash('Profile updated successfully!')
        return redirect(url_for('profile'))  # Redirect back to the profile page
    
    return render_template('profile.html', user=current_user)  # Render the profile page

@app.route('/create_plan', methods=['GET', 'POST'])
def create_plan():
    if request.method == 'POST':
        # Get data from the form
        current_weight = float(request.form['current_weight'])
        target_weight = float(request.form['target_weight'])
        age = int(request.form['age'])
        height = int(request.form['height'])
        gender = request.form['gender']
        activity_level = request.form['activity_level']
        dietary_preference = request.form['dietary_preference']
        
        # Calculate daily calories
        try:
            daily_calories = calculate_daily_calories(
                current_weight=current_weight,
                target_weight=target_weight,
                activity_level=activity_level,
                age=age,
                height=height,
                gender=gender
            )
        except ValueError as e:
            return f"Error: {e}"

        # Generate meal and workout plan
        user_plan = generate_plan(dietary_preference, activity_level)

        # Debugging: Print user_plan to check its structure
        print(user_plan)  # This will print the user_plan dictionary to your console/log

        # Render the plan page with the results
        return render_template('view_plan.html', plan=user_plan, daily_calories=daily_calories)

    return render_template('create_plan.html')  # Display the form on GET request


@app.before_request
def make_session_permanent():
    session.permanent = True  # Make the session permanent

# Route for viewing the user's plan
@app.route('/view_plan')
def view_plan():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))  # Redirect to login if no user is logged in

    # Now you can get user data directly from current_user
    user = current_user

    # Retrieve the necessary data from the user object
    current_weight = user.current_weight
    target_weight = user.target_weight
    age = user.age
    height = user.height
    gender = user.gender
    activity_level = user.activity_level
    dietary_preference = user.dietary_preference

    # Check if any required data is missing and provide specific error messages
    missing_data = []
    if current_weight is None:
        missing_data.append("current weight")
    if target_weight is None:
        missing_data.append("target weight")
    if age is None:
        missing_data.append("age")
    if height is None:
        missing_data.append("height")
    if gender is None:
        missing_data.append("gender")
    if activity_level is None:
        missing_data.append("activity level")
    if dietary_preference is None:
        missing_data.append("dietary preference")
    
    if missing_data:
        return f"Error: Missing required data: {', '.join(missing_data)}. Please ensure all profile fields are filled."

    # Calculate daily calories
    try:
        daily_calories = calculate_daily_calories(
            current_weight=current_weight,
            target_weight=target_weight,
            activity_level=activity_level,
            age=age,
            height=height,
            gender=gender
        )
        print(f"Calculated daily calories: {daily_calories}")
    except ValueError as e:
        return f"Error: {e}"

    # Generate meal and workout plan
    try:
        user_plan = generate_plan(activity_level, dietary_preference)
    except Exception as e:
        return f"Error generating plan: {str(e)}"

    # Return the plan along with the daily calories
    return render_template('view_plan.html', plan=user_plan, daily_calories=daily_calories)

# API route to get recommended plan based on user data (for future enhancements)
@app.route('/get_plan', methods=['POST'])
def get_plan():
    user_data = request.json
    age = int(user_data['age'])
    gender = user_data['gender']
    current_weight = float(user_data['current_weight'])
    target_weight = float(user_data['target_weight'])
    dietary_preference = user_data['dietary_preference']
    health_conditions = user_data.get('health_conditions', "")
    activity_level = user_data['activity_level']

    recommended_plan = generate_plan(age, gender, current_weight, target_weight, dietary_preference, health_conditions, activity_level)
    return jsonify(recommended_plan)

def generate_plan(dietary_preference, activity_level):
    plan = {}

    if dietary_preference == 'Vegan':
        meals = ['Vegan Buddha Bowl', 'Quinoa Salad', 'Lentil Soup']
    elif dietary_preference == 'Veg':
        meals = ['Mixed Vegetable Salad', 'Chickpea Curry', 'Paneer Tikka']
    else:
        meals = ['Grilled Chicken Salad', 'Egg Omelette', 'Fish Curry']

    plan['meals'] = meals

    # Adjust workout plan based on activity level
    if activity_level == 'Low':
        workouts = ['Walking', 'Stretching']
    elif activity_level == 'Medium':
        workouts = ['Jogging', 'Yoga']
    else:
        workouts = ['Running', 'Weight Training']

    plan['workouts'] = workouts

    return plan

# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)  # Pass current_user to the template
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    try:
        # Delete the user's account from the database
        db.session.delete(current_user)  # Delete the current user from the database
        db.session.commit()  # Commit the transaction to make the change permanent

        # Log out the user after account deletion
        logout_user()

        # Redirect to a page (e.g., home page or login page)
        flash('Your account has been deleted successfully.', 'success')
        return redirect(url_for('index'))  # Redirect to home or login page
    except Exception as e:
        # Handle any errors (e.g., failed database deletion)
        flash(f"Error deleting account: {e}", 'danger')
        return redirect(url_for('profile'))  # Redirect back to profile page if deletion fails

if __name__ == '__main__':
    app.run(debug=True, port=5001)
