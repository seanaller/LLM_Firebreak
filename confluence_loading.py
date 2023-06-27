## confluence_loading.py
## Description:
## - Retrieve data from list of confluence pages (returned as string)
##
## Setup
## - Supply a confluence API token stored in .env file as variable (str) CONFLUENCE_API_TOKEN

## Environment Setup
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import List

## Main Class Definition

class confluenceParser():
    """confluenceParser
    Class for parsing confluence pages. Steps for running:
    1. Setup using the .setup() method
    2. Load in pages to extract from using .update()
    3. Extract confluence page information using .extract()
    
    Note:   Confluence token should either be supplied in a .env file assigned to variable CONFLUENCE_API_TOKEN (prefered)
            or specified as a string using .setup() [._configureToken()]
    """    
    
    def __init__(self):
        """__init__

        Class instatisation
        """        
        self._page_urls = []
        self._token = None
        self._confluence_extract = ''
        self._headers_html = None
        
    ## Main Class Run Functions
    def setup(
        self,
        token_str: str = '',
        page_urls: List[str] = [],
    ):
        """setup()
        
        Setup the class for confluence page extraction

        Args:
            token_str (str, optional): Token string (if not specifying from .env file). Defaults to ''.
            page_urls (List[str], optional): List of confluence page URLs to extract. Defaults to [].
        """        
        # Set confluence api token
        self._configureToken(token_str)
        # Set the confluence pages to read
        if len(page_urls) != 0:
            self._pageList(page_urls)
        else:
            print('INFO: No URL list found - please update with confluence page URLs using ._pageList()')
            
    def update(
        self,
        page_urls: List[str] = []
    ):
        """update()
        
        Updates class with confluence page urls

        Args:
            page_urls (List[str], optional): List of confluence page URLs to extract. Defaults to [].

        """        
        if len(page_urls) > 0:
            self._pageList(page_urls)
        else:
            raise ValueError('ERROR: No URLs defined. Please specify a list of confluence page URLs to update class with.')
        
    def extract(self):
        if len(self._page_urls) > 0:
            self.read_pages()
            print('INFO: Confluence pages extracted and saved to self._confluence_extract')
        else:
            raise ValueError('ERROR: No URLs defined. Please specify a list of confluence page URLs to update class with.')
            
        
    ## Class Configuration Functions
    def _configureToken(
        self,
        token_str: str = ''
    ):
        """_configureToken()

        Args:
            token_str (str, optional): Confluence API token string - only supply if not specified in .env file. Defaults to ''.
        """        
        # Assign token from .env file (CONFLUENCE_API_TOKEN)
        if token_str == '':
            print('Loading token from .env file...')
            load_dotenv(override=True)
            token = os.getenv("CONFLUENCE_API_TOKEN")
            # Check of variable
            if token == None:
                raise ValueError('ERROR: No confluence api token found in .env file. Check assignment to variable CONFLUENCE_API_TOKEN...')
            else:
                self._token = token
                print('Token assigned from .env file...')
        # Assign token from input string
        elif len(token_str) > 1:
            print('Assigning token from input string...')
            self._token = token_str
        # Return error
        else:
            raise ValueError('ERROR: No token found. Check .env file or input token string...')
                
    def _pageList(
        self,
        page_urls: List[str]
        ):
        """_pageList
        
        Updates the list of confluence pages to extract from

        Args:
            page_urls (List[str]): List of full URLS for confluence pages
        """
        if len(self._page_urls) == 0:
            self._page_urls = page_urls
            print(f'Assigned {len(page_urls)} pages...')
        else:
            self._page_urls.extend(page_urls)
            print(f'Added {len(page_urls)} to page list..')
                
    ## Class Supporting Method Definitions
    def _configure_headers(self):
        self._headers_html =  {"Content-Type":"text/html", "Authorization": f"Bearer {self._token}"}
    
    def _readable_url(
        self,
        page_url: str
    ):
        return requests.utils.unquote(page_url.replace('+',' '))
    
    def _read_page(
        self,
        page_url: str,
        ):
        # Retrieve page contents
        if self._headers_html == None:
            raise ValueError('ERROR: HTML headers not generated (self._configure_headers)')
        else:
            response = requests.get(page_url,  headers=self._headers_html)
            content = BeautifulSoup(response.content,'html.parser')
        # Extract
        for script in content(["script", "style"]):
            script.extract()
        # Store in list(str)
        text = content.get_text()
        text = ' '.join(text.split())
        # Return
        return text
    
    def _read_pages(self):
        print(f'Extracting from {len(self._page_urls)} confluence pages...')
        for page_url in self._page_urls:
            try:
                page_base = self._readable_url(page_url)
                print(f'> Extracting content at {page_url} ...')
                self._confluence_extract += (self._read_page(page_url))
            except:
                raise ValueError(f'ERROR: Unable to parse page {page_base} @ {page_url}')
            
    def _split_text(
        self,
        max_chunk_size: int = 3000
    ):
        chunks = []
        current_chunk = ""
        for sentence in self._confluence_extract.split("."):
            if len(current_chunk) + len(sentence) < max_chunk_size:
                current_chunk += sentence + "."
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + "."
        if current_chunk:
            chunks.append(current_chunk.strip())
        self._confluence_chunks = chunks