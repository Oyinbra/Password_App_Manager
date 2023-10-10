# Import necessary modules
from flask import Flask, render_template, request, url_for, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import csv
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

# Create a Flask web application instance
app = Flask(__name__)

# Configure the SQLite database for the app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SECRET_KEY"] = "this is secret"

# Create a SQLAlchemy database instance
db = SQLAlchemy(app)


# Define the model/schema for the data
class PasswordManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(520), nullable=False)
    email = db.Column(db.String(520), nullable=False)
    site_url = db.Column(db.String(520), nullable=False)
    site_password = db.Column(db.String(520), nullable=False)

    def __repr__(self):
        return "<PasswordManager %r>" % self.email


# Define the routes for the web application


# Route for the home page
@app.route("/")
def index():
    passwordlist = PasswordManager.query.all()
    return render_template("index.html", passwordlist=passwordlist)


# Route for adding new details to the database
@app.route("/add", methods=["GET", "POST"])
def add_details():
    if request.method == "POST":
        # Get data from the form
        title = request.form["title"]
        email = request.form["email"]
        site_url = request.form["site_url"]
        site_password = request.form["site_password"]

        # Create a new entry in the database
        new_password_details = PasswordManager(
            title=title, email=email, site_url=site_url, site_password=site_password
        )
        db.session.add(new_password_details)
        db.session.commit()
        return redirect("/")


# Route for updating details (not implemented yet)
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_details(id):
    updated_details = PasswordManager.query.get_or_404(id)
    if request.method == "POST":
        updated_details.title = request.form["title"]
        updated_details.email = request.form["email"]
        updated_details.site_url = request.form["site_url"]
        updated_details.site_password = request.form["site_password"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an error updating the password details"
    return render_template("update.html", updated_details=updated_details)


# Route for deleting details (not implemented yet)
@app.route("/delete/<int:id>")
def delete_details(id):
    new_details_to_delete = PasswordManager.query.get_or_404(id)
    try:
        db.session.delete(new_details_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a error deleting the details"
    
@app.route("/export")
def export_data():
    with open('dump.csv', 'w') as f:
        out = csv.writer(f)
        out.writerow(['id', 'title', 'email', 'site_url', 'site_password'])
        for item in PasswordManager.query.all():
            out.writerow([item.id, item.title, item.email, item.site_url, item.site_password])
    return send_file('dump.csv',
        mimetype='text/csv',
        download_name=f"Export_Password_{timestr}.csv",
        as_attachment=True)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=8000)  # Run the app in debug mode for development
