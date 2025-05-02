# automation/generator.py

import openai
from openai.error import RateLimitError, AuthenticationError, APIError

from django.conf import settings

openai.api_key = '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'

def generate_blog_content():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": "You are an intelligent and helpful assistant, Please generate a catchy blog title and a short 3-paragraph blog post about a trending topic in Hair Diseases to urge clients to want to book a session with us to resolve their hair issues."
        }]
    )
    result = response.choices[0].message.content
    title, body = result.split("\n", 1)
    return title.strip(), body.strip()

def generate_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return response.choices[0].message['content']
    
    except RateLimitError:
        return "❌ Sorry, you've reached the usage limit for now. Please try again later."

    except AuthenticationError:
        return "❌ Authentication failed. Please check your API key or billing details."

    except APIError as e:
        return f"❌ OpenAI API error: {str(e)}"

    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"