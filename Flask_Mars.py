from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mission_scraping"
mongo = PyMongo(app)

mars_data = mongo.db.mars_data

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    mars_info = mars_data.find_one()

    # Return template and data
    return render_template("index.html", data_db=mars_info)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_dict = scrape()

    # Update the Mongo database using update and upsert=True
    mars_data.insert_many([mars_dict])
     
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
