import http.client
import urllib.parse
import json
import requests
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Constants
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPEN_AI_KEY= os.getenv("OPENAI_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
YOUR_SITE_URL = "https://jeezai.com"
YOUR_APP_NAME = "JeezAI"

def get_linkedin_user_details(linkedin_url):
    encoded_url = urllib.parse.quote(linkedin_url, safe='')
    conn = http.client.HTTPSConnection("fresh-linkedin-profile-data.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': "fresh-linkedin-profile-data.p.rapidapi.com"
    }
    conn.request("GET", f"/get-linkedin-profile?linkedin_url={encoded_url}&include_skills=false", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)

def get_linkedin_posts(linkedin_url):
    encoded_url = urllib.parse.quote(linkedin_url, safe='')
    conn = http.client.HTTPSConnection("fresh-linkedin-profile-data.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': "fresh-linkedin-profile-data.p.rapidapi.com"
    }
    conn.request("GET", f"/get-profile-posts?linkedin_url={encoded_url}&type=posts", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)

def generate_text(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "x-api-key": f"{OPEN_AI_KEY}",
    }
    data = {
        "model": "openai/gpt-4-turbo",
        "max_tokens": 6000,
        "temperature": 0,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()



def linkedin_analysis(url):
    #linkedin_url = input("Please enter the LinkedIn profile URL: ")
    linkedin_url = url
    user_details = get_linkedin_user_details(linkedin_url)
    user_details_no_urls = {key: value for key, value in user_details['data'].items() if not isinstance(value, str) or 'http' not in value}
    user_details_string = json.dumps(user_details_no_urls)
    posts_data = get_linkedin_posts(linkedin_url)
    posts = posts_data.get('data', [])


    print("\nExtracted Posts:")
    for i, post in enumerate(posts, 1):
        if 'text' in post:
            print(f"Post {i}: {post['text']}")
        else:
            print(f"Post {i}: [No text available]")

    if posts:
        prompt = f"""
        LinkedIn Profile Analysis

        User Summary:
        Change the below things accorinding to the user data,the below is just an example:
        - Name: John Doe
        - Profile Summary: Experienced AI professional with a passion for innovation.
        - Current Role: AI Researcher at Tech Innovations Inc.
        - Profile URL: {linkedin_url}
        - Education: Bachelor of Science in Computer Science, University of Tech, Master of AI, AI Institute
        - Experiences: AI Engineer at AI Solutions Co., Data Scientist at Data Insights Ltd(Please Try to get all the previous experience of the user and list them)
        - Interests: AI research, machine learning, data science

        Atleast write about 200 words for each of the following .First write the User Summary according to the user.

        Detailed Analysis Request:
        1. Analyze the technical content of the user's posts. Highlight any innovative ideas or significant contributions to the field of AI.
        2. Extract key phrases or important sentences that showcase the user's expertise and thought leadership.
        3. Assess the engagement levels of the posts (likes, comments, shares) to gauge influence and reach within the professional network.
        4. Identify any trends in the topics discussed over time and how they align with current industry trends.
        5. Evaluate the user's network growth and interactions to understand their community impact and collaborative efforts.


        Professional Interests:
        - List specific areas of AI and technology the user is interested in, based on post content and interactions.

        Skills & Expertise:
        - Detail technical skills, tools, and methodologies mentioned or implied in the user's posts.

        Professional Goals:
        - Infer potential career aspirations and professional development goals from the user's content and interactions.

        Please structure your response with clear headings and bullet points for each section.
        """
        prompt+=user_details_string
        for i, post in enumerate(posts, 1):
            try:
                prompt += f"\nPost {i}: {post['text']}"
            except KeyError:
                prompt += f"\nPost {i}: [No text available]"

        analysis_results = generate_text(prompt)
        if 'choices' in analysis_results:
            print("\nAnalysis Results:\n")
            analysis_messages = []
            for choice in analysis_results['choices']:
                analysis_messages.append(choice['message']['content'])  # Append each message to the list
                print(choice['message']['content'])

            analysis_results_string = "\n".join(analysis_messages)
            return analysis_results_string

        else:
            return("Failed to generate analysis results.(Might be due to Prompt tokens limit exceeded on openrouter api)")
    else:
        return("No posts found or no text available in posts.(Might be due to you rapidapi key monthly quota limit.)")


app = FastAPI()

class Query(BaseModel):
    query: str



@app.post("/")
def analyze(query: Query):
    url = query.query
    return linkedin_analysis(url)


