import json
import logging
import re
import requests

from typing import Dict, List, AnyStr
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

base_link = 'https://github.com'

base_headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
}

def process_input() -> Dict: 
    with open('input.json', 'r') as input_file:
        input = None
        
        try:
            input = json.loads(input_file.read())
        except:
            logging.error('Please input a valid data type. Only JSON-formatted data is allowed')
        
        if isinstance(input, dict):
            keywords = input.get('keywords', [])
            proxy_list = input.get('proxies', [])
            return fetch_data(keywords, proxy_list)
        elif isinstance(input, list):
            for member in input:
                keywords = member.get('keywords', [])
                proxy_list = member.get('proxies', [])
            return fetch_data(keywords, proxy_list)
        else:
            logging.error("JSON file can't be empty")
            
    
def fetch_data(keywords: List, proxy_list: List = None, type: AnyStr = None) -> Dict:
    out_list = {}
    
    for word in keywords:
        session = requests.Session()
        session.proxies = proxy_list
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        resp = session.get(base_link+'/search?q='+word, headers=base_headers)
        
        repo_list = re.findall(r'click-hmac="\w+"\shref="([^"]+)', resp.text)
        out_list.update({word:[base_link+i for i in repo_list]})
    
    return out_list


if __name__ == "__main__":
    with open ('output.json', 'w') as out_file:
        out_file.write(json.dumps(process_input()))
