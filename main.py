 raise self.handle_error_response(
openai.error.InvalidRequestError: This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?
from langchain import HuggingFaceHub

import json

with open('config.json', 'r') as f:
    config = json.load(f)
import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = config['HUGGINGFACEHUB_API_TOKEN']
repo_id = "google/flan-t5-xl"  # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options

llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0, "max_length": 64})
from langchain import PromptTemplate, LLMChain

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "Who won the FIFA World Cup in the year 1994? "

print(llm_chain.run(question))