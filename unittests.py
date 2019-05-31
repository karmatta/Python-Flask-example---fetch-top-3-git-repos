# Python unit tests for flask program to hit the github API to fetch the top 3 repos from org
# prerequisits: flask, requests, github API
# Author: Karthik D

import unittest 
from fetch_top_3_repos import fetch_repo_stars
from fetch_top_3_repos import fetch_repo_stars
import hashlib
import timeit
import json

# Define Functions to test
# function to post a request

def POST_request(email, url):
    #hashing the email
    emailhash = hashlib.md5(email.encode('utf-8')).hexdigest()
    # data to be sent to api 
    header = {'x-verloop-password':emailhash 
         } 

    body  = {"email": email,
            "name": "Karthik D",
            "angel_list": "https://angel.co/karthik-devaraj?al_content=view+your+profile&al_source=transaction_feed%2Fnetwork_sidebar",
            "github": "https://github.com/karmatta"
        }
  
    start = timeit.timeit()
    # sending post request and saving response as response object 
    try:
        response = requests.post(url, body, headers=header) 
        # extracting response text  
        print("response:", response.text ) 
        print("Time taken for response:", timeit.timeit()-start)
        return response.text
    except:
        print("invalid url")
        return ("invalid url")

# Define Functions to test
# Function to call the API to fetch the top 3 repos from org

def post_org_id(org_json, url):
    # sending post request and saving response as response object 
    try:
        response = requests.post(url, org_json) 
        return response.text
    except:
        return ("API server down or invalid")
        
# Define Unit Tests

class TestingMethods(unittest.TestCase): 
      
    def setUp(self): 
        pass
  
    # Returns True if equal
    def test_post_org_id(self): 
        self.assertEqual(post_org_id('{"org":"aaa"}', 'http://127.0.0.1:5001/') , "API server down or invalid")
        self.assertEqual(post_org_id('{"org":"Tuura"}', 'http:///') , "API server down or invalid")
        self.assertEqual(post_org_id('{"org":"aaa"}', 'http://127.0.0.1:5001/') , "API server down or invalid")
        
    # Returns True if equal. 
    def test_POST_request(self):     
        url = "https://hiring.verloop.io/api/github-challenge/start/"
        self.assertEqual(POST_request("karthikdmatta@gmail.com", url), "invalid url") 
        
if __name__ == '__main__':
    unittest.main()
  