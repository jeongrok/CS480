import urllib.request
import re


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

def main():
    h = downloadStockPage('AAPL', 'NASDAQ')
    saveToFile(h, 'aapl.html')
    price = getPrice(h)
    print('Price:', price)


if __name__ == "__main__":
    main()