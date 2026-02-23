from tavily import TavilyClient
from langchain_core.tools import tool
from langchain_community.document_loaders import WebBaseLoader
from datetime import datetime
import json
import os 
absolute_path = os.path.abspath(__file__)
current_path = os.path.dirname(absolute_path)

from dotenv import load_dotenv

load_dotenv()

@tool
def web_search(query: str):
    """
    주어진 query에 대해 웹 검색을 하고 결과를 반환한다.

    Args:
        query (str): 검색어 
    Returns:
        dict: 검색 결과 
    """
    client = TavilyClient()

    content = client.search(
        query,
        search_depth='advanced',
        include_raw_content=True,
    )

    results = content['results']

    for result in results:
        if result['raw_content'] is None:
            try:
                result['raw_content'] = load_web_page(result['url'])
            except Exception as e:
                print(f"Error loading page: {result['url']}")
                print(e)
                result['raw_conent'] = result['content']

    resource_json_path = f"{current_path}/data/resources_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}.json"

    with open(resource_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    return results, resource_json_path

def load_web_page(url: str):
    loader = WebBaseLoader(url, verify_ssl=False)

    content = loader.load()

    raw_content = content[0].page_content.strip()

    while '\n\n\n' in raw_content or '\t\t\t' in raw_content:
        raw_content = raw_content.replace('\n\n\n', '\n\n')
        raw_content = raw_content.replace('\t\t\t', '\t\t')

    return content

if __name__ == '__main__':
    results, resource_json_path = web_search.invoke("2026년 한국 경제 전망")
    print(results)

    # result = load_web_page('https://eiec.kdi.re.kr/publish/columnView.do?cidx=15029&c-code=&pp=20&pg=&sel_year=2025&sel_month=01')
    # print(result)