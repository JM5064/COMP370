import argparse
from bs4 import BeautifulSoup as bs
import json
import requests


def fetch_site(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    response = requests.get(url, headers=headers)

    return response


def obtain_articles(html_text):
    soup = bs(html_text, 'html.parser')

    # section with all covered stories: pm-cover-stories
    featured_section = soup.find('div', class_='pm-cover-stories')

    # each featured article: pm-card
    articles = featured_section.find_all('article', class_='pm-card')

    article_links = []

    for article in articles:
        a = article.find('a')
        article_link = a.get('href')

        article_links.append(article_link)

    return article_links


def retrieve_article_data(html_text):
    soup = bs(html_text, 'html.parser')

    # Get title
    title = soup.find('h1', class_='postmedia-article-topper__headline').text.strip()

    # Get author name
    author_name = soup.find('a', class_='author-meta__author').text.strip()

    # Get date
    date = soup.find('time', class_='author-meta__date').text.strip()

    # Get blurb
    blurb = soup.find('p', class_='postmedia-article-topper__excerpt').text.strip()

    return {
        "title": title, 
        "publication_date": date,
        "author": author_name,
        "blurb": blurb
    }


def save_to_file(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", type=str, help="Output file path", required=True)
    args = parser.parse_args()

    montreal_news_url = 'https://montrealgazette.com/category/news/'

    html_text = fetch_site(montreal_news_url).text

    article_urls = obtain_articles(html_text)

    article_data = []

    for article_url in article_urls:
        article_html = fetch_site(article_url)
        data = retrieve_article_data(article_html.text)

        article_data.append(data)
        
    save_to_file(article_data, args.o)



if __name__ == "__main__":
    main()

