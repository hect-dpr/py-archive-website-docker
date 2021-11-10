#!/usr/local/bin/python

import os, sys
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
from datetime import datetime

def is_url(url):
  try:
    result = urlparse(url)
    if all([result.scheme, result.netloc]):
        return result.netloc
  except ValueError:
    return False

def download_assets_and_count(url, pagefolder, tag2find='img', inner='src', for_count=False):

    if not os.path.exists(pagefolder):
        os.mkdir(pagefolder)
    
    count = 0

    for res in soup.findAll(tag2find):
        try:
            count += 1
            if not res.has_attr(inner):
                continue
            elif for_count:
                continue
            
            if res.get(inner).startswith('/'):
                filename = os.path.basename(res[inner])
                fileurl = urljoin(url, res.get(inner))
                filepath = os.path.join(pagefolder, filename)

                res[inner] = os.path.join(os.path.basename(pagefolder), filename)
                if not os.path.isfile(filepath):
                    with open(filepath, 'wb') as file:
                        filebin = session.get(fileurl)
                        file.write(filebin.content)
        except Exception as exc:
            print(exc, file=sys.stderr)
    
    return soup, count
    
session = requests.Session()

metadata = False
for arg in sys.argv:
    if arg == '--metadata':
        metadata = True
        continue
    url_netloc = is_url(arg)
    if not metadata and url_netloc:
        response = session.get(arg)
        now = datetime.utcnow().strftime('%a %b %d %Y %H:%M %Z')
        soup = BeautifulSoup(response.text, features="lxml")
        pagefolder = url_netloc + '_assets'
        soup, count_imgs = download_assets_and_count(arg, pagefolder, 'img', 'src')
        soup, count_imgs = download_assets_and_count(arg, pagefolder, 'img', 'srcset')
        soup, count_csses = download_assets_and_count(arg, pagefolder, 'link', 'href')
        soup, count_links = download_assets_and_count(arg, pagefolder, 'a', 'href', True)
        soup, count_scripts = download_assets_and_count(arg, pagefolder, 'script', 'src')
        html = soup.prettify().replace('window.pagePath="/"', 'window.pagePath=""') # ugly fix for gatsby sites which reloads to / on load
        with open(url_netloc+'.html', 'wb') as file:
            file.write(html.encode('utf-8'))
        with open(url_netloc+'.txt', 'w') as file:
            file.writelines('\n'.join([
                'site: ' + url_netloc,
                'num_links: ' + str(count_links),
                'images: ' + str(count_imgs),
                'last_fetch: ' + now + 'UTC',
                ]))
    elif metadata and url_netloc:
        try:
            with open(url_netloc+'.txt', 'r') as file:
                print(file.read())
        except:
            print(url_netloc + ' was not archived/ deleted!')