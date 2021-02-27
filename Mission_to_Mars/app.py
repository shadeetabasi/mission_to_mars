#import necessary libraries and py file
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars
import json
from pprint import pprint

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection (make sure we are establishing connection to collection and not db)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars_db")

@app.route("/")
def home():
    print("Welcome to the Mars Data Page!")
    # Find one record of data from the mongo database
    mars_data = mongo.db.mission_to_mars.find_one()
    new_hemispheres = [
        {"hemisphere_title": k, 
        "final_jpg_url":v} for 
        k,v in mars_data["mars_hemispheres"].items()
        ]
    mars_data["mars_hemispheres"] = new_hemispheres
    print(mars_data["mars_hemispheres"])


    # Return template and data
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mission_to_mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)
