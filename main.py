import getopt
import sys
import requests
from bs4 import BeautifulSoup
from series import Series
from helper import ParseImageLink

# For development
link = "https://docln.net/truyen/787-tensei-shitara-kendeshita"


def init():
    # Get novel link from argument ----------------------------------
    argumentlist = sys.argv[1:]

    # Options
    options = 'hdl:'

    # Long options
    long_options = ['help=', 'dev=', 'link=']

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentlist, options, long_options)

        # Get first argument
        for currentArgument, currentValue in arguments:
            if currentArgument in ('-h', '-help'):
                print('Baby shark dudududu')
                sys.exit()
            elif currentArgument in ('-d', '--dev'):
                url = link
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
                }
            elif currentArgument in ('-l', '--link'):
                url = currentValue
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
                }
            break

    except getopt.error as err:
        print('Invalid command line argument. Quitting...')
        sys.exit()

    return (url, headers)
    # ---------------------------------------------------------------


def main():
    url, headers = init()

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f'Status code: {response.status_code}')
        sys.exit()

    doc = BeautifulSoup(response.content, 'html.parser')

    series = Series()
    series.Title = doc.select_one(".series-name > a").text.strip()
    series.Translator = doc.select_one(".series-owner_name > a").text.strip()
    series.Group = doc.select_one(".fantrans-value > a").text.strip()
    series.Cover = ParseImageLink(
        doc.select_one('.series-cover > .a6-ratio > div'))
    series.Description = [p.text.strip()
                          for p in doc.select('.summary-content > p')]

    sharing_item = doc.select_one('.sharing-item')
    if sharing_item:
        attr = sharing_item.get("@click.prevent")
        if attr:
            attr = attr.strip()
            attr = attr.lstrip("window.navigator.clipboard.writeText('")
            attr = attr.rstrip("')")
            split = attr.split("/truyen/")
            series.BaseUrl = attr
            series.Id = split[1]

    info_items = doc.select('.info-item')
    if info_items:
        for item in info_items:
            name = item.select_one('.info-name').text.strip()
            value = item.select_one('.info-value > a').text.strip()
            match name:
                case 'Tác giả:':
                    series.Author = value
                case 'Họa sĩ:':
                    series.Artist = value
                case 'Tình trạng:':
                    series.Status = value
        print((series.Author, series.Artist, series.Status))


if __name__ == '__main__':
    main()
