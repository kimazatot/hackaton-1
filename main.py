import requests
from bs4 import BeautifulSoup as BS
import csv
from datetime import datetime

def get_html(url):
    response = requests.get(url)
    return response.text

def write_to_csv(data):
    with open('news.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Img'])
        writer.writerows(data)

def get_soup(html):
    soup = BS(html, 'lxml')
    return soup

def get_data(soup):
    news = soup.find_all('div', class_='Tag--article')
    data = []
    count = 0
    for new in news:
        try:
            title = new.find('a', class_='ArticleItem--name').text.strip()
        except:
            title = ''

        try:
            link = new.find('a', class_='ArticleItem--name').get('href')
        except:
            link = ''

        img = new.find('img').get('src')
        description_html = get_soup(get_html(link))
        description = description_html.find('div', class_='Article--text').text.replace('\n', '')
        data.append([title, img, description])
        count += 1
        if count == 20:
            break

    return data


def main():
    url = 'https://kaktus.media/?lable=8&date=2023-12-14&order=time'
    current_time = datetime.now()
    part1 = 'https://kaktus.media/?lable=8&date='
    part2 = f'{str(current_time.year)}-{str(current_time.month)}-{str(current_time.day)}'
    part3 = '&order=time'
    url = part1 + part2 + part3
    html = get_html(url)
    soup = get_soup(html)
    data = get_data(soup)
    return data
main()