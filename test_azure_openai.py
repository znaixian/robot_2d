from openai import AzureOpenAI
import json

with open('config.json') as f:
    config = json.load(f)

client = AzureOpenAI(
    api_version="2023-09-01-preview",
    azure_endpoint="https://azure-llm.factset.com/",
    api_key=config['AZURE_OPENAI_API_KEY']
)

try:
    response = client.chat.completions.create(
        model="gpt-4o-0513",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, world!"}
        ]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
