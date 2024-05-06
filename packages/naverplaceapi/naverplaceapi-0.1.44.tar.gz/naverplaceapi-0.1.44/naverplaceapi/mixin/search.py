import json
import urllib
import urllib.parse
import urllib.request
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import re
import sys
import os
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bs4 import BeautifulSoup


def url_encode_string(input_string):
    encoded_string = urllib.parse.quote(input_string)
    return encoded_string

#함수 정의
def delete_iframe(url, soup=None): #iframe 제거 후 blog.naver.com 붙이기
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    res = requests.get(url,headers=headers)
    res.raise_for_status()
    src_url = "https://blog.naver.com/"+soup.iframe["src"]
    soup = BeautifulSoup(res.text, "lxml")
    return src_url

def scraping(url): #본문 스크랩하는 함수
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    res = requests.get(url,headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    if soup.find("div", attrs={"class":"se-main-container"}): #본문 내용 있으면
        text = soup.find("div", attrs={"class":"se-main-container"}).get_text()
        text = text.replace("\n", "")
        return text
    else:
        return ""


class SearchMixin:
    CLIENT_ID = "ak4jckPbdjMcrMmFDSgv"
    CLIENT_SECRET = "Ye3VCcl2in"


    def search_blog_simple_unofficial(self, query):
        url = "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=" + quote(
            query)  # querys로 안해서 결과가 이상했다

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
        res = requests.get(url, headers=headers)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "lxml")

        blogs = soup.find_all("li", attrs={'class': 'bx'})  # class에 'bx' 들어가는 것
        # class가 <li class="bx">가 아닌 <li class="bx lineup">, <li class="bx term"> 들은 TypeError 발생
        contents = []
        for blog in blogs:
            try:
                blog_link = blog.find("a", attrs={'class': 'title_link'})["href"]
                blog_name = blog.find("a", attrs={'class': 'title_link'}).get_text()
                thumbnails = blog.find_all("img")

                avatar_source = thumbnails[0]['src']
                blog_thumbnails_source = list(map(lambda x:x['src'], thumbnails[1:]))
                # print(blog_name, blog_link)

                blog_text = blog.find("div", attrs={'class':"dsc_area"}).get_text()

                blog_p = re.compile("blog.naver.com")
                blog_m = blog_p.search(blog_link)
                contents.append({
                    'query': query, 'title': blog_name, 'link': blog_link, 'description': blog_text,
                    'avatar': avatar_source, 'thumbnail_sources':blog_thumbnails_source
                })
            except TypeError:  # TypeError: 'NoneType' object is not subscriptable 인 경우 무시
                pass
        return contents

    def get_place_detail_by_address(self, address, page_no=1):
        encoded_keyword = urllib.parse.quote(address)
        url = f'https://map.naver.com/p/api/entry/addressDetailPlace?address={encoded_keyword}&page={page_no}'
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            results = json.loads(response_body)
            return results
        else:
            return None



    def all_search(self,
                  query,
                  type,  # ex) all/place
                  searchCoord, #    ex. 126.942428;37.485309
                  boundary = None
                  ):
        encoded_keyword = urllib.parse.quote(query)
        # url = f"https://openapi.naver.com/v1/search/local.json?query={encoded_keyword}&display={page_size}"
        url = f"https://map.naver.com/p/api/search/allSearch?query={encoded_keyword}&type={type}&searchCoord={searchCoord}&boundary={boundary}"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            results = json.loads(response_body)
            return results['result']
        else:
            return None
    def search(self,
               keyword: str, page_size: int = 5,
               start:int = 10,
               client_id: str = CLIENT_ID, client_secret: str = CLIENT_SECRET,
               proxies=None):
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://openapi.naver.com/v1/search/local.json?query={encoded_keyword}&display={page_size}&start=5"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        result_list = []
        if rescode == 200:
            response_body = response.read()
            response_json = json.loads(response_body)
            results = json.loads(response_body)['items']

            for result in results:
                result['title'] = result['title'].replace('<b>', '').replace('</b>', '')
                result_list.append(result)
        return result_list
    def search_blog(self,
               keyword: str, page_size: int = 5,
               client_id: str = CLIENT_ID, client_secret: str = CLIENT_SECRET,
               proxies=None):
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://openapi.naver.com/v1/search/blog.json?query={encoded_keyword}&display={page_size}"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        result_list = []
        if rescode == 200:
            response_body = response.read()
            results = json.loads(response_body)['items']

            for result in results:
                result['title'] = result['title'].replace('<b>', '').replace('</b>', '')
                result_list.append(result)
        return result_list




    def scrape_google(self, subject):
        try:
            url_encoded_subject = url_encode_string(subject)
            # Search Operators https://moz.com/learn/seo/search-operators
            # Remove site: operator: '"+site%3Atwitter.com+OR+site%3Aseekingalpha.com+OR+site%3Areuters.com+OR+site%3Amarketscreener.com+OR+site%3Ayahoo.com'
            full_url = 'https://www.google.com/search?q="' + url_encoded_subject + '&tbm=vid"'
            print("Trying url " + full_url)

            # response = requests_get(full_url)
            response = requests.get(full_url)

            links = []

            soup = BeautifulSoup(response.content, 'html5lib')

            father_divs = soup.find_all('div', {'class': 'MjjYud'})
            for father_div in father_divs:
                upper_div = father_div.find('div', {'class': 'Z26q7c UK95Uc jGGQ5e'})
                upper_subdiv = upper_div.find('div', {'class': 'yuRUbf'})

                lower_div = father_div.find('div', {'class': 'Z26q7c UK95Uc'})
                lower_subdiv = lower_div.find('div', {'class': 'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf'})
                lower_spans = lower_subdiv.find_all('span')
                lower_div_text = ''
                for lower_span in lower_spans:
                    lower_ems = lower_span.find_all('em')
                    lower_div_text += ' '.join([em.text.strip() for em in lower_ems])

                upper_div_a = upper_subdiv.find('a', {'href': lambda href: href})
                if upper_div_a:
                    upper_div_text = upper_div_a.find('h3').text.strip()

                    google_result = upper_div_text + ". " + lower_div_text
                    # similarity = similarity_score(subject, google_result)
                    print("Google result:", google_result)
                    # if similarity > 0.75:
                    #     print("Relevant")
                    #     link = upper_div_a['href']
                    #     return scraping_by_url(link, subject)

            print("Link not found")
            return "N/A", subject
        except Exception as e:
            print("Exception in scrape_google:", e)
            return "N/A", subject