from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")


@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_overview.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    
    mars_data = scrape_mars.scrape()
    mongo.db.mars_overview.update({}, mars_data, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)