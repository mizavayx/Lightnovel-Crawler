import re

reUrl = re.compile("url\\('(.*?)'\\)")

def ParseImageLink(selection):
    attr = selection.get('style')
    if attr and reUrl.search(attr):
        return reUrl.findall(attr)[0]
    return "https://docln.net/img/nocover.jpg"