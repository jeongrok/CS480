import urllib.request
import re
import requests
from bs4 import BeautifulSoup


# Example:
# html = downloadStockPage('AAPL', 'NASDAQ')
def downloadStockPage(ticker, exchange):
    url = f'https://www.google.com/finance/quote/{ticker}:{exchange}'
    print('Downloading:', url)
    r = urllib.request.urlopen(url)
    html = r.read().decode('utf-8')
    return html


def saveToFile(text, filename):
    fh = open(filename, 'w')
    fh.write(text)
    fh.close()


def getPrice(html):
    p = r'data-last-price="([\d\.]+)"'
    m = re.search(p, html)
    if m != None:
        return float(m.group(1))
    else:
        return None

def websiteArxiv(keyword):
    url = f'https://arxiv.org/search/cs?query={keyword}&searchtype=title&abstracts=show&order=-announced_date_first&size=50'
    r = urllib.request.urlopen(url)
    html = r.read().decode('utf-8')
    return html

def getTitles(html):
    regex = r'<p\sclass="title\sis-5\smathjax">\s*(.*?)<span\sclass="search-hit\smathjax">BERT<\/span>(.*?)\s*<\/p>'
    result = re.findall(regex, html)
    for title in result:
        temp = ''.join(title)
        print(temp)


# xml aware package --> beautiful soup: meaning that it works on generic xml

def bs4getTitles(keyword):
    url = f'https://arxiv.org/search/cs?query={keyword}&searchtype=title&abstracts=show&order=-announced_date_first&size=50'
    temp = requests.get(url)
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(temp.content, 'html.parser')
    # Extract all titles from the search results page
    titles = [title.text.strip() for title in soup.find_all('p', {'class': 'title is-5 mathjax'})]
    # Print the extracted titles
    print(len(titles))
    for title in titles:
        print(title)

def main():
    # h = downloadStockPage('TSLA', 'NASDAQ')
    # # saveToFile(h, 'aapl.html')
    # price = getPrice(h)
    # print('Price:', price)

    # failed attempt to use regex to crawl titles with BERT
    # h = websiteArxiv('BERT')
    # getTitles(h)
    bs4getTitles('BERT')


if __name__ == "__main__":
    main()


def isBalanced(self, root):

    def dfs(node)