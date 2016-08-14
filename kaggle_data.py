#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Stefan Jansen'

import shutil
from os import environ, listdir, makedirs
from os.path import join, expanduser, exists, isdir
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup as soup
from pandas import *

## Set path for data file storage
analysis_dir = expanduser('~/kaggle')

## Create path if necessary
if not exists(analysis_dir):
    makedirs(analysis_dir)


def get_data_dir(competition):
    data_dir = join(analysis_dir, competition, 'data')
    if not exists(data_dir):
        makedirs(data_dir)
    return data_dir


def download_data(competition='talkingdata-mobile-user-demographics', filetype=['.zip']):
    """Download kaggle competition data files of designated type(s)

    Assumes that KAGGLE_USER and KAGGLE_PASSWD can be retrieved via os.environ[] as environment variables
    Requires prior acceptance of terms and conditions for specific competition and user

    :param competition: kaggle competition url name
    :param filetype: desired data file formats for download - list
    """

    data_dir = get_data_dir(competition)
    kaggle_url = 'https://www.kaggle.com'
    login_url = '/'.join(s.strip('/') for s in [kaggle_url, 'account', 'login'])
    data_url = '/'.join(s.strip('/') for s in [kaggle_url, 'c', competition, 'data'])
    login_data = dict(UserName=environ['KAGGLE_USER'], Password=environ['KAGGLE_PASSWD'])

    with requests.session() as s:
        s.post(login_url, data=login_data)
        response = s.get(data_url)
        html = soup(response.text, 'html.parser')
        links = [a.get('href') for a in html.find_all('a') if a.get('href', None) and a.get('href').endswith(tuple(filetype))]

        for link in links:
            file_name = link.split('/')[-1]
            print('Downloading:', file_name)
            with open(join(data_dir, file_name), 'wb') as f:  # open binary type file for compressed
                response = s.get(urljoin(kaggle_url, link), stream=True)  # send download request
                shutil.copyfileobj(response.raw, f)  # download uncompressed


def data_to_hdf(competition='talkingdata-mobile-user-demographics'):
    """Uncompress competition data and store in HDFStore"""

    data_dir = get_data_dir(competition)
    with HDFStore(join(data_dir, 'source.h5')) as store:
        for f in [l for l in listdir(data_dir) if not isdir(l) and not l.startswith('.') and not l.endswith('.h5')]:
            file_name = f.split('.')[0]
            print('Storing:', file_name)
            try:
                store.put(file_name, read_csv(join(data_dir, f)))
            except Exception as e:
                print(f, '\n', e)

if __name__ == '__main__':
    download_data()
    data_to_hdf()
