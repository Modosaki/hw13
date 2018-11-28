from flask import Flask, render_template, redirect, jsonify
import pymongo

from flask_pymongo import PyMongo
import m_scrape

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")
# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)
# db = client.mars
# collection = db.mars


# # Route to render index.html template using data from Mongo
# @app.route("/")
# def home():

#     # Find one record of data from the mongo database
#     md = mongo.db.collection.find_one()
#     # md = list(db.collection.find())

#     # Return template and data
#     return render_template("index.html", mars_d=md)


# # Route that will trigger the scrape function
# @app.route("/scrape")
# def scrape():

#     # Run the scrape function
#     mars_data = m_scrape.scrape_info()
   

#     # Update the Mongo database using update and upsert=True
#     # mongo.db.collection.update({}, mars_data, upsert=True)
    

#     db.collection.insert_many(mars_data)

#     # Redirect back to home page
#     return redirect("/")

@app.route("/")
def index():
    try:
        mars_data = mongo.db.mars_data.find_one()
        return render_template('index.html', mars_data=mars_data)
    except:
        return redirect("http://localhost:5000/scrape", code=302)

@app.route("/scrape")
def scraped():
    mars_data = mongo.db.mars_data
    mars_data_scrape = m_scrape.scrape_info()
    mars_data.update(
        {},
        mars_data_scrape,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)










if __name__ == "__main__":
    app.run(debug=True)
