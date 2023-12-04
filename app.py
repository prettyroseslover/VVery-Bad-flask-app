from flask import Flask, render_template, request, redirect, url_for
import os
from vuln.xss.xss import xss_page
from vuln.idor.idor import idor_page, idor_api, idor_next_page
from vuln.sqli.sqli import sqli_page, sqli_api
from vuln.osci.osci import os_page
from vuln.pathtrav.pathtrav import path_traversal_page, path_traversal_image
from vuln.bruteforce.bruteforce import brute_page, brute_api

from db_helper import db_helper
from db_models import db_models


app = Flask(__name__)

app.config['PUBLIC_IMG_FOLDER'] = f"{os.getcwd()}/static/img"

db_helper.initialize()
app.db_helper = db_helper
app.db_models = db_models


@app.route("/")
def home_page():
    return render_template('home.html')

# XSS
@app.route('/xss', methods=['GET'])
def xss():
    return xss_page(request, app)

#IDOR
@app.route('/idor', methods=['GET', 'POST'])
def idor():
    if request.method == 'GET':
        return idor_page(request, app)

    return idor_api(request, app)

@app.route('/idor_profile', methods=['GET'])
def idor_profile():
    return idor_next_page(request, app)

#SQLI 
@app.route('/sqli', methods=['GET', 'POST'])
def sqli():
    if request.method == 'GET':
        return sqli_page(request, app)

    return sqli_api(request, app)

#OS command injection
@app.route('/os', methods=['GET'])
def os_injection():
   return os_page(request, app)


#Path Traversal
@app.route('/pathtraversal', methods=['GET'])
def path_traversal():
    return path_traversal_page(request, app)

@app.route('/pathtraversalimg', methods=['GET'])
def path_traversal_img():
    return path_traversal_image(request, app)

#Brute Force
@app.route('/bruteforce', methods=['GET', 'POST'])
def brute_force():
    if request.method == 'GET':
        return brute_page(request, app)

    return brute_api(request, app) 

if __name__ == "__main__":
    app.run(debug=True)