from openai import OpenAI
import user_config

# # Initialize the client
# client = OpenAI(
#     api_key=user_config.deepseek_v3,
#     base_url="https://openrouter.ai/api/v1",
# )

# def send_request(query):
#     messages = [
#         {"role": "user", "content": query},
#         {"role": "assistant", "content": "```python\n", "prefix": True}
#     ]
    
#     completion = client.chat.completions.create(
#         model="deepseek/deepseek-v3-base:free",
#         messages=messages,
#         stop=["```"],
#     )

#     return completion.choices[0].message.content

# def send_request2(messages):
#     completion = client.chat.completions.create(
#         model="deepseek/deepseek-v3-base:free",
#         messages=messages,
#         stop=["```"],
#     )

#     return completion.choices[0].message.content


client = OpenAI(
    api_key=user_config.deepseek,
    base_url="https://openrouter.ai/api/v1",
)

def send_request(query):
    messages = [
        {"role": "user", "content": query},
        {"role": "assistant", "content": "```python\n", "prefix": True}
    ]
    
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=messages,
        stop=["```"],  
    )

    return completion.choices[0].message.content

def send_request2(messages):
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=messages,
        stop=["```"],
    )

    return completion.choices[0].message.content


