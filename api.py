from openai import OpenAI
import openai
from dotenv import load_dotenv
import os 

load_dotenv()
my_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
messages = [
    {'role': 'system', 'content': 'You are helping someone working in a small to medium size business, who is trying to understand how to do tasks that are part of their job.'}
]
while True:
    message=input('User :')
    if message: 
        messages.append(
            {'role':'user', 'content': message},
        )                                                                                   
        chat = client.chat.completions.create(
            model='gpt-3.5-turbo', messages=messages
        )

    reply=chat.choices[0].message.content
    print(f'ChatGPT:{reply}')
    messages.append({'role':'assistant', 'content':reply})