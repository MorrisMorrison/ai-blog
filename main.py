#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import openai
import re
import requests
import json
import schedule
import time
from urllib.parse import urljoin
import argparse

chatgpt_api_key = os.environ.get("CHATGPT_API_KEY")
hashnode_api_key = os.environ.get("HASNODE_API_KEY")
# publicationId can either be retreived via hashnode api or from the url of the publication / blog dashboard
hashnode_publication_id = os.environ.get("HASNODE_PUBLICATION_ID")

generate_content_prompt_path = 'generate-content-prompt.txt'
generated_posts_path = 'generated-posts/'

def main():
    if not check_environment_variables():
        return
    
    parser = argparse.ArgumentParser(description="AI-Blog Script")
    parser.add_argument("--scheduled", action="store_true", help="Run the script in scheduled mode")

    args = parser.parse_args()

    if args.scheduled:
        schedule.every().sunday.at("20:00").do(main)

        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        main()

    content = generate_content()
    if content == "":
        print("Content is empty. Skipping post creation.")
        return
    # check if content contains valid markdown syntax   
    if not re.search(r'^#.*', content, re.MULTILINE):
        print("Content is not valid markdown. Skipping post creation.")
        return
    
    title = extract_title(content)
    if title == "Untitled":
        print("Title is empty. Skipping post creation.")
        return
    
    store_content_as_file(title, content)
    post_to_hashnode(title, content)

def check_environment_variables():
    # if variable is unset or empty string, log and return false
    if not chatgpt_api_key:
        print("CHATGPT_API_KEY is not set. Skipping post creation.")
        return False
    if not hashnode_api_key:
        print("HASNODE_API_KEY is not set. Skipping post creation.")
        return False
    if not hashnode_publication_id:
        print("HASNODE_PUBLICATION_ID is not set. Skipping post creation.")
        return False
    return True 

def extract_title(markdown_content):
    match = re.search(r'^#\s+(.*)', markdown_content, re.MULTILINE)
    
    if match:
        return match.group(1).strip()
    else:
        return "Untitled"

def generate_content():
    content_prompt = read_file_content(generate_content_prompt_path)
    content = execute_chatgpt_prompt(content_prompt)
    return content

def execute_chatgpt_prompt(prompt):
    openai.api_key = chatgpt_api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1200,  # Adjust the max tokens based on your desired length
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

def post_to_hashnode(title, content):
    query = {
        "query": "mutation PublishPost($input: PublishPostInput!) { publishPost(input: $input) { post { id title } } }",
        "variables": {
            "input": {
                "title": title,
                "contentMarkdown": content,
                "publicationId": hashnode_publication_id,
                "tags": [
                    {
                        "slug": "test",
                        "name": "test"
                    }
                ]
            }
        }
    }
    print(query)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'{hashnode_api_key}'
    }

    response = requests.post(hashnode_url, headers=headers, json=query)

    if response.status_code == 200:
        # TODO check if errors is empty -> contains all validations
        print('Blog post created successfully on Hashnode!')
        print(response.text)
    else:
        print(f'Error creating blog post. Status code: {response.text}')


def read_file_content(path):
    file = open(path, 'r')
    content = file.read()
    file.close() 
    return content

def store_content_as_file(title, content):
    path = "generated-posts/" + title.lower().replace(" ", "_").replace("\"", "").replace("'", "") + ".md"
    with open(path, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    main()