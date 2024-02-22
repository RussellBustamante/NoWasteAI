import sys
import json
from openai import OpenAI

TOGETHER_API_KEY = "API_KEY"

client = OpenAI(api_key=TOGETHER_API_KEY,
  base_url='https://api.together.xyz',
)

def recommendation(days, ppm, prompt1):
    global chat_completion
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a food safety assistant. I have a food item that's past its best-before date. I will give you context like the room temperature and how long it's been out of the fridge or how many days after it's been. Tell me realistically if it's still edible and not dangerous, or if you should eat it at all",
            },
            {
                "role": "user",
                "content": f"I have a pizza slice that's {days} days past its best-before date. The exposure level (ppm) is {ppm}, which might or might not be considered still healthy. This was an opinion of another food assistant worker, \"{prompt1}\" Can I still eat it without any harm?",
            }
        ],
        model="meta-llama/Llama-2-70b-chat-hf",
        max_tokens=1024
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    # data = json.loads(sys.argv[1])
    days = sys.argv[1]
    ppm = sys.argv[2]
    result = recommendation(days, ppm)
    print(result)  # Print the response to stdout
