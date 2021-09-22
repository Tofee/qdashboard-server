# server-side web-services for QDashboard

from flask import Flask, Response, request
import urllib.request
import base64
import xmltodict
import json

app = Flask(__name__)

@app.route("/rss_tile/content/<string:rss_url_base64>")
def rss_tile_content(rss_url_base64):
    rss_url = base64.standard_b64decode(rss_url_base64).decode("utf-8", "ignore")
    print("Retrieving RSS URL: "+rss_url)

    rss_url_quoted = urllib.parse.quote(rss_url, safe='/:&')
    
    with urllib.request.urlopen(rss_url_quoted) as response:
        rss_xml = response.read()

    xml_as_dict = xmltodict.parse(rss_xml)
    json_string = json.dumps(xml_as_dict)
    
    return Response(json_string, mimetype='text/json')

@app.route("/weather_tile/forecast/<string:openweatherApiKey>/<string:place>")
def weather_tile_content(openweatherApiKey, place):
    openweather_url = "https://api.openweathermap.org/data/2.5/forecast?q=" + place + "&appid=" + openweatherApiKey
    
    with urllib.request.urlopen(openweather_url) as response:
        json_string = response.read()
    
    return Response(json_string, mimetype='text/json')

@app.route("/session/save", methods=['POST'])
def session_save():
    json_data = json.dumps(request.json)
    print("Session data to save: " + json_data)

    with open("session.json", "w") as outfile:
        outfile.write(json_data)
    
    return '', 204

@app.route("/session/read")
def session_read():
    # Opening JSON file
    with open('session.json', 'r') as openfile:
        json_object = json.load(openfile)

    json_string = json.dumps(json_object)
    return Response(json_string, mimetype='text/json')
