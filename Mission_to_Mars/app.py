#import necessary libraries and py file
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection (make sure we are establishing connection to collection and not db)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")


if __name__ == "__main__":
    app.run(debug=True)
