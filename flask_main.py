import re
import requests
from flask import Flask
from bs4 import BeautifulSoup as bs

app = Flask(__name__)


def repl(m):
    return m.group(0) + "™"


def replace_sources(bs_obj):
    for text in bs_obj.find_all(text=re.compile(r'\b[\w]{6}\b')):
        text.replace_with(re.sub(r'\b[\w]{6}\b', repl, text))
    return bs_obj


def replace_hrefs(bs_obj):
    for a in bs_obj.find_all('a', 'href' is not None):
        a['href'] = a['href'].replace("https://habr.com", "http://localhost:5000")
    return bs_obj


@app.route('/')
@app.route('/<path:subpath>')
def show_all(subpath=""):
    path = "http://habr.com/" + subpath
    b = bs(requests.get(path).text, "html.parser")
    b = replace_sources(b)
    b = replace_hrefs(b)
    html = b.prettify("utf-8")
    return html


if __name__ == '__main__':
    app.run()
