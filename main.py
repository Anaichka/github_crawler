import re
import json
import logging
import requests

from lxml import html
from urllib import parse
from typing import Dict, List, AnyStr
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

base_link = 'https://github.com'

base_headers = {
    'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
}
logger = logging.getLogger('Petlyura')
logging.basicConfig(level=logging.INFO)

def process_input(filename) -> Dict: 
    with open(filename, 'r') as input_file:
        input = None
        
        try:
            input = json.loads(input_file.read())
        except json.JSONDecodeError:
            logger.error('Please input a valid data type. Only JSON-formatted data is allowed')
        
        if isinstance(input, dict):
            keywords = input.get('keywords', [])
            proxy_list = input.get('proxies', [])
            return fetch_data(keywords, proxy_list)
        elif isinstance(input, list):
            keywords = []
            proxy_list = []
            for member in input:
                keywords+=member.get('keywords', [])
                proxy_list+=member.get('proxies', [])
            return fetch_data(keywords, proxy_list)
        else:
            logger.error("JSON file can't be empty")
            
    
def fetch_data(keywords: List, proxy_list: List = None, type: AnyStr = None) -> Dict:
    out_dict = {}
    
    session = requests.Session()
    session.proxies = proxy_list
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    for word in keywords:
        resp = session.get(parse.urljoin(base_link,'/search'), params={"q": word}, headers=base_headers)
        repo_list = re.findall(r'click-hmac="\w+"\shref="([^"]+)', resp.text)
        if repo_list:
            repo_info = []
            for elem in repo_list:
                link = parse.urljoin(base_link, elem)
                author = elem.split('/')[1]
                repo_resp = session.get(link, headers=base_headers)
                tree = html.fromstring(repo_resp.text)
                languages = tree.xpath('//span[@class="Progress"]/span')
                language_stats = {}
                for selector in languages:
                    lang = selector.attrib['aria-label'].split()[0]
                    stat = selector.attrib['aria-label'].split()[-1]
                    language_stats.update({lang:stat})

                repo_info.append({'url': link, 'extra': { 'owner': author,'language_stats': language_stats}})
            out_dict[word] = repo_info
        else:
            logger.error("There are no links found")
    
    return out_dict


if __name__ == "__main__":
    with open ('output.json', 'w') as out_file:
        logger.info("Let's crawl some Github content! Starting...")
        result = process_input(filename='input.json')
        if result:
            out_file.write(json.dumps(result))
            logger.info("Success! Enjoy your data!")
        else:
            logger.info("Oops, something gone wrong. Check logs below!")
