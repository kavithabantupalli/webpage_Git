from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
from pymongo import MongoClient

app = Flask(__name__)

# Initialize MongoDB client and database
my_client = MongoClient("localhost", 27017)
my_db = my_client["form"]
registration_collection = my_db["registrations"]  # Collection for registrations
login_collection = my_db["logins"]  # Collection for login attempts

@app.route("/", methods=["GET"])
def homepage():
    return "<h1>Welcome to Form Registration</h1>"

@app.route("/home", methods=["GET"])
def frontend():
    return render_template("index.html")

@app.route("/reg", methods=["POST"])
def get_reg_data():
    # Get user registration data from form
    name = request.form["u_name"]
    email = request.form["u_email"]
    phone = request.form["u_num"]
    password = request.form["u_pwd"]

    # Create a user dictionary
    user = {
        "user_name": name,
        "user_email": email,
        "user_phone": phone,
        "user_pwd": password
    }

    # Insert user data into the MongoDB registrations collection
    registration_collection.insert_one(user)
    return redirect("/home")

@app.route("/login", methods=["POST"])
def get_login_data():
    # Get login credentials from form
    log_email = request.form["u_email"]
    log_password = request.form["u_pwd"]

    # Check credentials against the MongoDB registrations collection
    user = registration_collection.find_one({"user_email": log_email, "user_pwd": log_password})

    if user:
        # Log the successful login attempt
        login_collection.insert_one({"user_email": log_email, "status": "Success"})
        return "Login Successful 😊"
    else:
        # Log the failed login attempt
        login_collection.insert_one({"user_email": log_email, "status": "Failure"})
        return "Invalid Credentials 😞"

@app.route("/view", methods=["GET"])
def view_database():
    # Retrieve all registrations from the MongoDB collection
    all_users = list(registration_collection.find({}, {"_id": 0}))  # Exclude the MongoDB ID field
    return {"registrations": all_users}

if __name__ == "__main__":
    app.run(debug=True)
