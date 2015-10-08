import urllib2
import os
import json
from flask import Flask, render_template, jsonify, Response, request
try:
    import MySQLdb
    db = MySQLdb.connect(host='dursley.socs.uoguelph.ca',
                         user='mfriedma',
                         passwd='0828745',
                         db='mfriedma')
    cur = db.cursor()

except:
    pass


app = Flask(__name__)


API_KEY = "3f65f46fe00a2d83627eec8fd0b85714:14:72956778"
NYT_BASE_URL = "http://api.nytimes.com/svc/search/v2/articlesearch.json?api-key={}".format(API_KEY)


@app.route("/dynamic")
def dynamic():
    return render_template('dynamic.html')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/static")
def static_data():
    return render_template('static.html')


@app.route("/api/Search/<string:term>")
def search(term):
    if term == "mock":
        return mock()
    return search_nyt(term)


def search_nyt(term):
    found_from_db = get_from_db(term)
    if found_from_db is None:
        search_path = "{}&fq={}".format(NYT_BASE_URL, term)
        response = urllib2.urlopen(search_path)
        data = response.read()
        save_to_db(term, data)
    else:
        data = found_from_db

    return _parse_nyt(data)


def get_from_db(search):
    cur.execute("SELECT * FROM searches WHERE keyword=%s", (search,))
    results = cur.fetchall()
    return results[0]['data'] if len(results) > 0 else None


def save_to_db(keyword, data):
    cur.execute("INSERT INTO searches (keyword, data) VALUES (%s, %s)", (keyword, data,))
    cur.commit()


def mock():
    root = os.path.realpath(os.path.dirname(__file__))
    data = open(os.path.join("static/sample_data.json"), "r").read()
    return _parse_nyt(data)


def _parse_nyt(data):
    data = json.loads(data)
    responses = []
    data = data.get("response")
    docs = data.get("docs", [])
    for doc in docs:
        doc_data = {
            "id": doc.get("_id", None),
            "headline": _extract_headline(doc),
            "snippet": doc.get("snippet", ""),
        }
        responses.append(doc_data)

    return generate_response({"data": responses}, 200)


def _extract_headline(doc):
    return doc.get("headline", {}).get("main", "")
    

def _extract_name_from_byline(doc):
   byline = doc.get("byline", {})
   print byline
   return byline.get("original", "")


def generate_response(body, code):
    json_response = jsonify(body)
    json_response.status_code = code

    return json_response



if __name__ == '__main__':
    app.run(debug=True)

