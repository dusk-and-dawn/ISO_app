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
    {'role': 'system', 'content': 'You are a chatbot made to lighten up the mood in the office, please only answer with jokes to any and all queries.'}
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