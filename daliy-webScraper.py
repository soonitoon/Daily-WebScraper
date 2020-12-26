import requests
from bs4 import BeautifulSoup
import re

def create_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    # 흐림, 어제보다 00도 높아요.
    cast = soup.find("p", attrs={"class":"cast_txt"}).get_text()
    curr_temp = soup.find("p", attrs={"class":"info_temperature"}).get_text().replace("도씨", "") # 현재온도
    min_temp = soup.find("span", attrs={"class":"min"}).get_text() # 최저온도
    max_temp = soup.find("span", attrs={"class":"max"}).get_text() # 최고 온도
    # 오전오후 강수확률 %
    mor_rain_rate = soup.find("span", attrs={"class":"point_time morning"}).get_text().strip() # 오전 강수
    aft_rain_rate = soup.find("span", attrs={"class":"point_time afternoon"}).get_text().strip() # 오후 강수

    # 미세먼지 정보
    dust = soup.find("dl", attrs={"class":"indicator"})
    pm10 = dust.find_all("dd")[0].get_text() # 미세
    pm25 = dust.find_all("dd")[1].get_text() # 초미세
    # 출력
    print(cast)
    print("현재 {} (최저 {} / 최고 {})".format(curr_temp, min_temp, max_temp))
    print("오전 {} / 오후 {}".format(mor_rain_rate, aft_rain_rate))
    print()
    print("미세먼지 : {}".format(pm10))
    print("미세먼지 : {}".format(pm25))
    print()

def create_news(idx, title, link):
    print("{}. {}".format(idx + 1, title))
    print("  (링크 : {})".format(link))
    print()

def scrape_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://news.naver.com"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"hdline_article_list"}).find_all("li", limit=3)
    for idx, news in enumerate(news_list):
        title = news.find("a").get_text().strip()
        link = url + news.find("a")["href"]
        create_news(idx, title, link)

def scrape_it_news():
    print("[it 뉴스]")
    url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"type06_headline"}).find_all("li", limit=3)
    for idx, news in enumerate(news_list):

        img = news.find("dt",attrs={"class":"photo"})
        dt_idx = 0
        if img:
            dt_idx = 1

        title = news.find_all("a")[dt_idx].get_text().strip()
        link = news.find_all("a")[dt_idx]["href"]
        create_news(idx, title, link)

def scrape_english():
    print("[오늘의 영어회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
    soup = create_soup(url)
    sentences = soup.find_all("div",attrs={"id":re.compile("^conv_kor_t")})
    print("(영어지문)")
    for sentence in sentences[len(sentences)//2:]: # 8 문장이 있다고 가정할 때, 5~8
        print(sentence.get_text().strip())
    print()
    print("(한글지문)")
    for sentence in sentences[:len(sentences)//2]:
        print(sentence.get_text().strip())
        
if __name__ == "__main__":
    scrape_weather() # 오늘의 날씨 정보 가져오기
    scrape_headline_news() # 헤드라인 뉴스 정보 가져오기
    scrape_it_news()
    scrape_english() # 오늘의 영어 회화 가져오기