#%%
from langchain.llms import OpenAI
import json

with open('config.json', 'r') as f:
    config  = json.load(f)

# export OPENAI_API_KEY=config['OPENAI_API_KEY']
llm = OpenAI(temperature=0.9, openai_api_key=config['OPENAI_API_KEY'], model='davinci')
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# 
print(llm.predict('what is an egg'))

# chat = ChatOpenAI(temperature=0, openai_api_key=config['OPENAI_API_KEY'])
# chat.predict_messages([HumanMessage(content="Translate this sentence from English to French. I love programming.")])
# >> AIMessage(content="J'aime programmer.", additional_kwargs={})