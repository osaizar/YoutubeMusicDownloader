from flask import Flask, request, jsonify, render_template, url_for, redirect, make_response
import commands as c
import requests
import traceback

import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

PORT = 5000
ADDR = "0.0.0.0"

app = Flask(__name__)

CLIENT_ID = "a60d7050138d495eab2a3e0177ad05ae"
CLIENT_SECRET='39d8f28ed80e45a1a251879fbf429a8d'
REDIRECT_URI='http://localhost:5000/auth'

SCOPE = 'user-library-read'

AUTH = None
@app.route("/")
def index():
    return render_template("index.html"), 200

@app.route("/auth")
def auth():
    try:
        data = request.args
        token_info = AUTH.get_access_token(data["code"])
        token = token_info["access_token"]

        response = make_response(redirect('/'))
        response.set_cookie('authtoken', token)
        return response

    except Exception, e:
        tb = traceback.format_exc()
        print tb
        return render_template("error.html", code=500, message="Errorea zerbitzarian"), 500


# REST Routes

@app.route("/get_login_url", methods=["GET"])
def get_login_url():
    try:
        return jsonify({"url" : AUTH.get_authorize_url()}), 200
    except Exception, e:
        tb = traceback.format_exc()
        print tb
        return jsonify({"error" : "Errorea zerbitzarian"}), 500

@app.route("/get_playlists", methods=["POST"])
def get_playlists(): # input: username
    try:
        data = request.get_json(silent = True)
        if 'authtoken' not in request.cookies: # TODO: validator.py
            return jsonify({"error" : "Txokolatezko gaileta falta da"}), 400

        token = request.cookies["authtoken"]

        list =  []
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(data["username"])

        for playlist in playlists['items']:
            list.append({"name" : playlist["name"], "id" : playlist["id"], "owner" : playlist["owner"]["id"]})
            print str(playlist)

        return jsonify({"message" : "success", "playlists" : list}), 200
    except Exception, e:
        tb = traceback.format_exc()
        print tb
        return jsonify({"error" : "Errorea zerbitzarian"}), 500

@app.route("/download_playlist", methods=["POST"])
def download_playlist():
    try:
        data = request.get_json(silent = True)
        data["playlist_id"]

        if 'authtoken' not in request.cookies:
            return render_template("error.html", code=500, message="Txokolatezko gaileta falta da"), 400


    except Exception, e:
        tb = traceback.format_exc()
        print tb
        return render_template("error.html", code=500, message="Errorea zerbitzarian"), 500

# Static Routes
@app.route("/lib/bootstrap/css/bootstrap.css")
def bootstrapCSS():
    return app.send_static_file("css/bootstrap/bootstrap.css")

@app.route("/lib/bootstrap/js/bootstrap.js")
def bootstrapJS():
    return app.send_static_file("js/bootstrap/bootstrap.js")

@app.route("/css/client.css")
def clientCSS():
    return app.send_static_file("css/client.css")

@app.route("/js/client.js")
def clientJS():
    return app.send_static_file("js/client.js")

@app.route("/js/main.js")
def mainJS():
    return app.send_static_file("js/main.js")

if __name__ == '__main__':
    AUTH = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE)
    app.run(host=ADDR, port=PORT)
