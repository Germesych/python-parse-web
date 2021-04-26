import requests
from bs4 import BeautifulSoup
import json

URL = 'https://jobs.dev.by/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537', 'accept': '*/*'}
HOST = 'https://jobs.dev.by'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS)
    return r


def get_content(html, null=None):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='vacancies-list-item--marked')

    job_openings = []

    for item in items:
        if item.find('span', class_='vacancies-list-item__label') is None:
            work = ""
        else:
            work = item.find('span', class_='vacancies-list-item__label').get_text(strip=True),

        job_openings.append({
            'title': item.find('a', class_='vacancies-list-item__link_block').get_text(strip=True),
            'company': item.find('a', class_='js-vacancy__footer__company-name').get_text(strip=True),
            'work': work,
            'link': HOST + item.find('a', class_='vacancies-list-item__link_block').get('href'),
        })
    return job_openings


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        job_openings = get_content(html.text)
        return job_openings

    else:
        print('Error', html.status_code)


with open('pars.json', 'w') as file:
    json.dump(parse(), file, indent=2, ensure_ascii=True)

if __name__ == '__main__':
    print(parse())
