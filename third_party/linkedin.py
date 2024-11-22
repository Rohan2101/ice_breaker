from dotenv import load_dotenv
import os
import requests

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url):
    r = requests.get(
        "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json")
    data = r.json()
    return data
if __name__=='__main__':
    print(scrape_linkedin_profile())