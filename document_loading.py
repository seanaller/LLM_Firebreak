from langchain.document_loaders import TextLoader

from urllib.parse import urlparse
import os
import pickle
import faiss
from config import config

import langchain
from typing import List
from bs4 import BeautifulSoup

from langchain.document_loaders import BSHTMLLoader
import requests

import json


def get_all_urls_from_base_url(base_url):
    url_list = []
    url = base_url +'sitemap.xml'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml-xml')
    for url_here in soup.find_all("loc"):
        if url_here:
            url_list.append(url_here.text)
    return url_list


def load_urls(urls: List[str]):
    loader = langchain.document_loaders.UnstructuredURLLoader(urls=urls)
    return loader.load()

def split_docs(data):
    splitter = langchain.text_splitter.CharacterTextSplitter(
        separator = '\n',
        chunk_size = 1000,
        chunk_overlap=200
    )
    return splitter.split_documents(data)


def get_embeddings_for_documnts(docs, path):
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    print('getting embeddings')
    embeddings_getter = OpenAIEmbeddings(openai_api_key=config.get_openai_api_key())
    embeddings = FAISS.from_documents(docs, embeddings_getter)
    with open(path, 'wb') as f:
        pickle.dump(embeddings, f)
    return embeddings

def answer_query(query, embedding_store):
    from langchain.chains import RetrievalQAWithSourcesChain 
    from langchain import OpenAI
    llm = OpenAI(
        temperature=0.3,
        openai_api_key=config.get_openai_api_key(),
        # model='gpt-3.5-turbo'
    )
    chain= RetrievalQAWithSourcesChain.from_llm(
        llm=llm,
        retriever=embedding_store.as_retriever()
    )
    response =  chain(
        {"question": query},
        return_only_outputs=True
    )
    print('Query:')
    print(query)
    print('Response')
    print(response['answer'])
    print('Sources:')
    print(response['sources'])


def get_name_from_url(url):
    netloc = urlparse(url).netloc
    main_domain = netloc.split(".")[-2] if 'www.' in netloc else netloc.split(".")[0]
    return main_domain


def get_embeddings_for_base_url(base_url):
    name = get_name_from_url(base_url)
    path = 'data/' + name + '.pkl'
    if os.path.exists(path):
        print('embeddings found')
        with open(path, 'rb') as f:
            embeddings = pickle.load(f)
        return embeddings
    else:
        urls = get_all_urls_from_base_url(base_url=base_url)
        urls = urls[0:10]
        data = load_urls(urls)
        split_data = split_docs(data)
        embeddings = get_embeddings_for_documnts(docs=split_data, path=path)
        return embeddings




base = "https://www.england.nhs.uk/"
embeds = get_embeddings_for_base_url(base_url=base)
response = answer_query(
    query='What is NHS England?',
    embedding_store=embeds
)
print(response)