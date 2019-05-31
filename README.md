# Python-Flask-example---fetch-top-3-git-repos
Repo consisting of flask programs to fetch top 3 repos from git given an org name as a JSON POST request

This project consists of API which returns top 3 repositories of an organisation in
Github by stars.

 The .py file "fetch_top_3_repos.py" is run to start the API server that fethes the top 3 repos of an organization from GitHub

## To start the server:

    run: python fetch_top_3_repos.py
    The server is hosted on http://127.0.0.1:5001/ by default

## To POST a request to the server:

    Call the function post_org_id(org_json, url), once the server is running
    The time for response is shown on the console.

The project also constists of unit tests for the functions.

The logger logs the status and the errors
