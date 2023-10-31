import openai
import requests
import json

# Set up your API keys
chatgpt_api_key = 'your_chatgpt_api_key'
hashnode_api_key = 'your_hashnode_api_key'

# Function to generate content using ChatGPT API
def generate_blog_content(prompt):
    openai.api_key = chatgpt_api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=500,  # Adjust the max tokens based on your desired length
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

# Function to post content to Hashnode using their API
def post_to_hashnode(title, content):
    hashnode_url = 'https://api.hashnode.com/'
    create_post_endpoint = 'v1/blog'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {hashnode_api_key}'
    }

    data = {
        'title': title,
        'contentMarkdown': content,
        'tags': ['python', 'chatgpt', 'automation'],  # Add relevant tags
        'publishDate': None,  # You can set a publish date if needed
        'coverImage': None,  # URL to the cover image
    }

    response = requests.post(f'{hashnode_url}{create_post_endpoint}', headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print('Blog post created successfully on Hashnode!')
    else:
        print(f'Error creating blog post. Status code: {response.status_code}')
        print(response.text)

# Example usage
prompt = "Write a blog post about the benefits of using ChatGPT in Python scripting."
generated_content = generate_blog_content(prompt)

blog_title = "Exploring the Power of ChatGPT in Python Automation"
post_to_hashnode(blog_title, generated_content)
