#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Stefan Jansen'

import shutil
from os import environ, listdir
from os.path import join
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup as soup
from pandas import *

analysis_dir = '/home/kaggle/analysis'


def download_data(competition='expedia-hotel-recommendations', filetype='.gz'):
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


def data_to_hdf():
    with HDFStore(join(analysis_dir, 'source.h5')) as store:
        for f in [l for l in listdir(analysis_dir) if l.endswith('.csv')]:
            file_name = f.split('.')[0]
            df = read_csv(join(analysis_dir, f))
            store.put(file_name, df)


if __name__ == '__main__':
    download_data()
    data_to_hdf()
