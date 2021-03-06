from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    mars_scrape = mongo.db.mars_scrape.find_one()

    return render_template("index.html", mars_scrape=mars_scrape)


@app.route("/scrape")
def scraper():

    mars_scrape = mongo.db.mars_scrape
    mars_title_data = scrape_mars.scrape()

    mars_scrape.update({}, mars_title_data, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
