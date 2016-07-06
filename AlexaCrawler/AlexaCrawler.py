from lxml.html import parse
from urllib2 import urlopen
import pandas
import requests

from BeautifulSoup import BeautifulSoup

base_url = 'http://www.alexa.com/topsites/global;{0}'
li_list = []
for page_no in xrange(20):
    # page_no = 0
    response = requests.get(base_url.format(page_no))
    html = response.content
    parsed_html = BeautifulSoup(html)
    lis = parsed_html.findAll('li', {'class': 'site-listing'})
    for li in lis:
        try:
            li_list.append(li.find('a').text)
        except 'KeyError':
            print li

print len(li_list)

with open('data/top-500.csv', 'wb') as bw:
    for li in li_list:
        bw.write('%s\n' % li.lower())
