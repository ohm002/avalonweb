from flask import *
from bs4 import BeautifulSoup
import requests
from github import Github
import json
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = "ultrasecretoooooooohhh"
configfile = json.loads(open("config.json").read())
CLIENT_ID = configfile["CLIENT_ID"]
CLIENT_SECRET = configfile["CLIENT_SECRET"]

@app.route("/")
def home():
	if session.get("logged") == "True":
		return render_template("displaylogin.html", username=session.get("username"), id=session.get("id"));
	else:
		return render_template("login.html")

@app.route("/loginpage/login")
def login():
	url_redirect = (
		f"https://osu.ppy.sh/oauth/authorize?client_id=8976&redirect_uri=http://127.0.0.1:5000/loginpage/auth&scope=identify&response_type=code"
	)
	return redirect(url_redirect)

@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/loginpage/")
def loginpage():
	return session.get("username")

@app.route("/loginpage/auth")
def auth():
	code = request.args.get("code")
	post_data = {
		"client_id": CLIENT_ID,
		"client_secret": CLIENT_SECRET,
		"code": code,
		"grant_type": "authorization_code",
		"redirect_uri": 'http://127.0.0.1:5000/loginpage/auth'
	}
	r = requests.post("https://osu.ppy.sh/oauth/token", json=post_data)
	print(r.text)
	js = r.json()
	access_token = js['access_token']

	# Example, get username
	r = requests.get("https://osu.ppy.sh/api/v2/me",
					 headers={"Authorization": f"Bearer {access_token}"})
	s = requests.get("https://osu.ppy.sh/api/v2/news", headers={
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json"
	})
	res = r.json()
	session["username"] = res["username"]
	session["id"] = res["id"]
	session["logged"] = "True"

	return redirect("/")

@app.route("/loginpage/logout")
def logout():
	session.pop("username")
	session.pop("id")
	session.pop("logged")
	return redirect("/index")

if __name__ == '__main__':
	app.run(debug = True)