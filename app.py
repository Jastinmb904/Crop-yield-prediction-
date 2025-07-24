from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy # type: ignore warning
from flask_bcrypt import Bcrypt # type: ignore warning
import numpy as np
import pickle
import os
# import re
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Load yield_df.csv and extract unique Area and Item values
try:
    yield_df = pd.read_csv("yield_df.csv")
    AREA_OPTIONS = sorted(yield_df["Area"].dropna().unique().tolist())
    ITEM_OPTIONS = sorted(yield_df["Item"].dropna().unique().tolist())
except Exception as e:
    app.logger.error(f"Failed to load yield_df.csv: {e}")
    AREA_OPTIONS = []
    ITEM_OPTIONS = []
# Configure session - Use a strong, random secret key in production
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")  # Set your own secret key
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
Session(app)

# Load ML models
def load_models():
    try:
        model_path = os.path.join(os.getcwd(), 'dtr.pkl')
        preprocessor_path = os.path.join(os.getcwd(), 'preprocessor.pkl')
        
        if not os.path.exists(model_path) or not os.path.exists(preprocessor_path):
            app.logger.error("Model files not found")
            return None, None
            
        with open(model_path, 'rb') as f:
            dtr = pickle.load(f)
        with open(preprocessor_path, 'rb') as f:
            preprocessor = pickle.load(f)
        return dtr, preprocessor
    except Exception as e:
        app.logger.error(f"Error loading models: {e}")
        return None, None

dtr, preprocessor = load_models()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Create database tables within application context
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return redirect(url_for("login"))

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        
        if not username or not email or not password:
            flash("Username, email, and password are required", "danger")
            return redirect(url_for("register"))
        
        if len(password) < 8:
            flash("Password must be at least 8 characters", "danger")
            return redirect(url_for("register"))

        # password_errors = []

        # if len(password) < 8:
        #     password_errors.append("at least 8 characters")
        # if not re.search(r"[A-Z]", password):
        #     password_errors.append("one uppercase letter")
        # if not re.search(r"[a-z]", password):
        #     password_errors.append("one lowercase letter")
        # if not re.search(r"[0-9]", password):
        #     password_errors.append("one number")
        # if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        #     password_errors.append("one special character")

        # if password_errors:
        #     if len(password_errors) == 1:
        #         message = f"Password must contain {password_errors[0]}."
        #     else:
        #         message = (
        #             "Password must contain "
        #             + ", ".join(password_errors[:-1])
        #             + f", and {password_errors[-1]}."
        #         )
        #     flash(message, "danger")
        #     return redirect(url_for("register"))

        # Check if user exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            flash("Username or email already taken!", "danger")
            return redirect(url_for("register"))

        # Hash password and store user
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            db.session.rollback()
            flash(f"Registration failed: {str(e)}", "danger")
            return redirect(url_for("register"))

    return render_template("register.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required", "danger")
            return redirect(url_for("login"))

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id  
            session["username"] = username  
            return redirect(url_for("predict"))
        else:
            flash("Invalid username or password!", "danger")

    return render_template("login.html")

# Prediction route
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    if dtr is None or preprocessor is None:
        flash("Prediction model is not available. Please contact the administrator.", "danger")
        return render_template("predict.html")

    # Initialize variables to store form data
    form_data = {
        'Year': '',
        'average_rain_fall_mm_per_year': '',
        'pesticides_tonnes': '',
        'avg_temp': '',
        'Area': '',
        'Item': ''
    }

    prediction_result = None

    if request.method == "POST":
        try:
            # Capture form data before processing
            form_data['Year'] = request.form.get('Year', '')
            form_data['average_rain_fall_mm_per_year'] = request.form.get('average_rain_fall_mm_per_year', '')
            form_data['pesticides_tonnes'] = request.form.get('pesticides_tonnes', '')
            form_data['avg_temp'] = request.form.get('avg_temp', '')
            form_data['Area'] = request.form.get('Area', '')
            form_data['Item'] = request.form.get('Item', '')

            year = int(form_data['Year'])
            if year < 1900 or year > 2100:
                flash("Year must be between 1900 and 2100", "danger")
                return render_template("predict.html", prediction=None, form_data=form_data)

            rainfall = float(form_data['average_rain_fall_mm_per_year'])
            if rainfall < 0:
                flash("Rainfall cannot be negative", "danger")
                return render_template("predict.html", prediction=None, form_data=form_data)

            pesticides = float(form_data['pesticides_tonnes'])
            if pesticides < 0:
                flash("Pesticides cannot be negative", "danger")
                return render_template("predict.html", prediction=None, form_data=form_data)

            temp = float(form_data['avg_temp'])
            if temp < -50 or temp > 60:
                flash("Temperature must be between -50°C and 60°C", "danger")
                return render_template("predict.html", prediction=None, form_data=form_data)

            area = form_data['Area'].strip()
            if not area:
                flash("Area cannot be empty", "danger")
                return render_template(
                    "predict.html",
                     prediction=None,
                     username=session.get("username"),
                     form_data=form_data,
                     area_options=AREA_OPTIONS,
                     item_options=ITEM_OPTIONS
                     )

            item = form_data['Item'].strip()
            if not item:
                flash("Item cannot be empty", "danger")
                return render_template("predict.html", prediction=None, form_data=form_data)

            features = np.array([[year, rainfall, pesticides, temp, area, item]], dtype=object)
            transformed_features = preprocessor.transform(features)
            prediction_result = round(dtr.predict(transformed_features)[0], 2)

        except Exception as e:
            app.logger.error(f"Prediction error: {e}")
            flash(f"An error occurred during prediction: {str(e)}", "danger")
            return render_template("predict.html", prediction=None, form_data=form_data)

    return render_template("predict.html",
    prediction=prediction_result,
    username=session.get("username"),
    form_data=form_data,
    area_options=AREA_OPTIONS,
    item_options=ITEM_OPTIONS
)

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    is_production = os.getenv("FLASK_ENV") == "production"
    app.run(debug=not is_production, host='0.0.0.0' if is_production else '127.0.0.1')
