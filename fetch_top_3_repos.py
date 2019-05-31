# Python flask program to hit the github API to fetch the top 3 repos from org
# prerequisits: flask, requests, github API
# Author: Karthik D

from flask import Flask, request
import requests
import json
import time
import sys
import operator
from github import Github
import logging

logging.basicConfig(filename='fetch_top_3_repos.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    sys.stderr.write("Response time: %ss\n" % resp_time)
    return response

def record_request_data(response):
    sys.stderr.write("Request path: %s Request method: %s Response status: %s\n" % (request.path, request.method, response.status_code))
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    # The order here matters since we want stop_timer
    # to be executed first
    app.after_request(record_request_data)
    app.after_request(stop_timer)
    
app = Flask(__name__)
setup_metrics(app)

# Function to create json from results
# [args]repo_stars - dictionary containing the top 3 repos
# returns json in required format

def make_response(repo_stars):
    resp_list = []
    for item in repo_stars.items():
        resp_list.append(dict({"name": item[0], "stars": item[1]}))
    return json.dumps((dict({"results": resp_list})))

# Fetch the top 3 repos based on star ratings
# [arg]request - json containing the org name
# returns json response

def fetch_repo_stars(request):
    
    GH_USERNAME = ''
    GH_PASSWORD = ''
    try:
        # fetch org name
        GH_ORG = json.loads(request).get('org')
        
    except:
        logging.error("Input not JSON or invalid, please input in the form")
        return json.dumps(dict({"results":"Input not JSON or invalid, please input in the form: {'org': 'github-organization-id'}"}))
    
    # Create git object
    g = Github(GH_USERNAME, GH_PASSWORD)
    repo_name =[]
    repo_stars =[]
    try:
        # hit git
        org = g.get_organization(GH_ORG) 
        # Fetch repos
        repos = org.get_repos()
        
    except:
        logging.error("Unauthorized or non-existant organization")
        return json.dumps(dict({"results":"Unauthorized or non-existant organization, try another one"}))
    
    for repo in repos:
        repo_name.append(repo.name)
        repo_stars.append(repo.stargazers_count)
        
    # Fetch the top 3 repos
    repo_dict = dict(zip(repo_name, repo_stars))
    sorted_repo_stars = sorted(repo_dict.items(), key=lambda kv: kv[1], reverse=True)
    if len(sorted_repo_stars) >= 3:
        repo_dict = dict(sorted_repo_stars[:3])
        return make_response(repo_dict)
    else:
        repo_dict = dict(sorted_repo_stars)
        return make_response(repo_dict)

# App trigger

@app.route("/", methods=['GET', 'POST'])
def wrapper():
    req = request.get_data()    #'{"org":"Tuura"}'
    return fetch_repo_stars(req)

if __name__ == '__main__':
    app.run(port=5001, debug=True)