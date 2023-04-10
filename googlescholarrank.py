import requests, os, datetime, argparse
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import warnings

#Default Parameters
KEYWORD = 'Chat GPT'
NRESULTS = 50
CSVPATH = '/Users/jeongrokyu/Desktop/23Spring/pythonProject'
STARTYEAR = None
now = datetime.datetime.now()
ENDYEAR = now.year
MAX_CSV_FNAME = 255

# Websession Parameters
GSCHOLAR_URL = 'https://scholar.google.com/scholar?start={}&q=allintitle%3A{}&hl=en&as_sdt=0,5'
STARTYEAR_URL = '&as_ylo={}'
ENDYEAR_URL = '&as_yhi={}'


def get_command_line_args():
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('--kw', type=str)
    parser.add_argument('--sortby', type=str)
    parser.add_argument('--nresults', type=int, help='Default is 50')
    parser.add_argument('--startyear', type=int, help='Default is None')
    parser.add_argument('--endyear', type=int, help='Default is current year')
    args, _ = parser.parse_known_args()
    keyword = KEYWORD
    if args.kw:
        keyword = args.kw
    nresults = NRESULTS
    if args.nresults:
        nresults = args.nresults
    start_year = STARTYEAR
    if args.startyear:
        start_year = args.startyear
    end_year = ENDYEAR
    if args.endyear:
        end_year = args.endyear

    return keyword, nresults, start_year, end_year


def get_citations(content):
    out = 0
    for char in range(0, len(content)):
        if content[char:char + 9] == 'Cited by ':
            init = char + 9
            for end in range(init + 1, init + 6):
                if content[end] == '<':
                    break
            out = content[init:end]
    return int(out)


def get_year(content):
    for char in range(0, len(content)):
        if content[char] == '-':
            out = content[char - 5:char - 1]
    if not out.isdigit():
        out = 0
    return int(out)


def get_author(content):
    for char in range(0, len(content)):
        if content[char] == '-':
            out = content[2:char - 1]
            break
    return out


def main():
    keyword, number_of_results, start_year, end_year = get_command_line_args()

    # Create main URL based on command line arguments
    if start_year:
        GSCHOLAR_MAIN_URL = GSCHOLAR_URL + STARTYEAR_URL.format(start_year)
    else:
        GSCHOLAR_MAIN_URL = GSCHOLAR_URL
    if end_year != now.year:
        GSCHOLAR_MAIN_URL = GSCHOLAR_MAIN_URL + ENDYEAR_URL.format(end_year)

    # Start new session
    session = requests.Session()
    links = []
    title = []
    citations = []
    year = []
    author = []
    rank = [0]
    # Get content from number_of_results URLs
    for n in range(0, number_of_results, 10):
        print("Loading...")
        url = GSCHOLAR_MAIN_URL.format(str(n), keyword.replace(' ', '+'))
        page = session.get(url)
        c = page.content
        # Create parser
        soup = BeautifulSoup(c, 'html.parser', from_encoding='utf-8')
        mydivs = soup.findAll("div", {"class": "gs_or"})
        for div in mydivs:
            try:
                links.append(div.find('h3').find('a').get('href'))
            except:  # catch *all* exceptions
                links.append('Look manually at: ' + url)
            try:
                title.append(div.find('h3').find('a').text)
            except:
                title.append('Could not catch title')
            try:
                citations.append(get_citations(str(div.format_string)))
            except:
                warnings.warn("Number of citations not found for {}. Appending 0".format(title[-1]))
                citations.append(0)
            try:
                year.append(get_year(div.find('div', {'class': 'gs_a'}).text))
            except:
                warnings.warn("Year not found for {}, appending 0".format(title[-1]))
                year.append(0)
            try:
                author.append(get_author(div.find('div', {'class': 'gs_a'}).text))
            except:
                author.append("Author not found")
            rank.append(rank[-1] + 1)
        sleep(5)

    # Create a dataset and sort by the number of citations
    data = pd.DataFrame(list(zip(author, title, citations, year, links)), index=rank[1:], columns=['Author', 'Title', 'Citations', 'Year', 'Source'])
    data.index.name = 'Rank'
    data_ranked = data.sort_values(by='Citations', ascending=False)
    path_csv = os.path.join(CSVPATH, keyword.replace(' ', '_') + '.csv')
    path_csv = path_csv[:MAX_CSV_FNAME]
    data_ranked.to_csv(path_csv, encoding='utf-8')


if __name__ == '__main__':
    main()