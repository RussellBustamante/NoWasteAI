import base64
import sys
import requests
import json
from flask import jsonify

# OpenAI API Key
api_key = "API_KEY"

def decode(bin):
    with open(bin, "rb") as image_file:
        base64_image = image_file.read().decode('utf-8')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Looking at this image of a food item, do you believe that it looks edible?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    json_object = response.json()
    content = json_object["choices"][0]["message"]["content"]
    return content

if __name__ == "__main__":
    bin = 'encode.bin'
    result = decode(bin)
    print(result)
