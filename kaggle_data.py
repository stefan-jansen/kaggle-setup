#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Stefan Jansen'

from os import environ
from os.path import join
from urllib.parse import urljoin

import shutil
import requests
from bs4 import BeautifulSoup as soup

analysis_dir = '/home/kaggle/analysis'

def download(competition='expedia-hotel-recommendations', filetype='.gz'):
    kaggle_url = 'https://www.kaggle.com'

    login_url = '/'.join(s.strip('/') for s in [kaggle_url, 'account', 'login'])
    data_url = '/'.join(s.strip('/') for s in [kaggle_url, 'c', competition, 'data'])
    login_data = dict(UserName=environ['KAGGLE_USER'], Password=environ['KAGGLE_PASSWD'])

    with requests.session() as s:
        s.post(login_url, data=login_data)
        response = s.get(data_url)
        html = soup(response.text, 'html.parser')
        links = [a.get('href') for a in html.find_all('a') if a.get('href', None) and a.get('href').endswith(filetype)]

        for link in links:
            filename = link.split('/')[-1]
            with open(join(analysis_dir, filename), 'wb') as f:  # open binary type file for compressed
                response = s.get(urljoin(kaggle_url, link), stream=True)  # send download request
                shutil.copyfileobj(response.raw, f)  # download uncompressed


if __name__ == '__main__':
    download()

