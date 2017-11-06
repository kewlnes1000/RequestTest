import json
from multiprocessing import Pool
import requests
import re
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        res = requests.get(url,headers = headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile(
        '<tbody.*?normalthread.*?title="(.*?)">.*?</div>.*?blockTitle.*?<em>.*?</em>'
        '.*?href="(.*?)".*?lastpost_time.*?href=".*?">(.*?)</a>.*?</tbody>',re.S
    )
    results = re.findall(pattern, html)
    for item in results :
        yield {
            '小說':item[0],
            '最後發表時間':item[2],
            '網址':item[1]
        }

def write_in_file(conntent):
    with open('requests.txt','a',encoding = 'utf-8') as f:
        f.write(json.dumps(conntent,ensure_ascii=False) + '\n' )
        f.close()

def main(offset):
    url = 'https://ck101.com/forum-237-%d.html' %offset
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_in_file(item)


if __name__ == '__main__' :
    pool = Pool()
    pool.map(main, [i+1 for i in range(143)])
    pool.close()
    pool.join()
