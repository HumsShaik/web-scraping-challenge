from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask Setup -- Create an instance of Flask
app = Flask(__name__)

# Database Setup -- Use PyMongo to establish Mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
#mongo = PyMongo(app)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")



# Flask Routes -- Route to render index.html template for initial scraping
@app.route("/")
def home():

    mars_hemisphere_dict = mongo.db.mars_hemisphere_dict.find_one()

    # Return template and data
    return render_template("index.html", mars_hemisphere_dict=mars_hemisphere_dict)
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Running the scrape function
    mars_hemisphere_dict = scrape_mars.scrape()
     
    # Update the mongo database using update and upsert 
    mongo.db.mars_hemisphere_dict.update({}, mars_hemisphere_dict, upsert=True)
    
    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
