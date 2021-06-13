from flask import Flask, render_template, redirect
from scrape_mars import MongoConnector
import scrape_mars


import pymongo

app = Flask(__name__)

_mongo_conn = MongoConnector()
_mongo_conn.database = 'mars_db'
_db = _mongo_conn.database

@app.route('/')
def index():
    latest_news = _db['headline'].find_one()
    featured_image = _db['featured_image'].find_one()
    mars_facts = _db['mars_facts'].find_one({}, {'_id': False})
    hemisphere_images = list(_db['hemisphere_images'].find())

    return render_template('index.html', latest_news=latest_news, featured_image=featured_image, mars_facts=mars_facts,
                           hemisphere_images=hemisphere_images)

@app.route('/scrape')
def scrape_new_data():
    scrape_mars.scrape()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)