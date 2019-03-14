#!/usr/bin/python
# -*- coding: utf-8 -*-

# SERVER_PORT
SERVER_PORT = 8000

# UPDATE PASSWORD
UPDATEPASSWORD = ''

# DB INFO
DB_HOST = ''
DB_USERNAME = ''
DB_PASSWORD = ''
DB_DATABASE = ''

# DB DBEXECUTE
LIMIT = " LIMIT 10;"
DBEXECUTE = "" + LIMIT
DBEXECUTE_F = "" + LIMIT
DBEXECUTE_LIVE = "" + " LIMIT 5;"

# URLs
URL_SITEURL = "https://musou.tw/"
URL_PHOTOLINK = "https://cdn.musou.tw/uploads/focus/photo_thumb/"
URL_FOCUSES = "https://musou.tw/focuses/"
URL_VIDEO = "https://musou.tw/videos/"
URL_LIVE = "https://musou.tw/live_streams/"
URL_LIVEPHOTO = "https://cdn.musou.tw/uploads/live_stream/photo_thumb/"

# CATEGORY
CATEGORY_LABLE_F = u'場邊焦點｜'
CATEGORY_LABLE_V = u'無雙影音｜'

CATEGORY = [{'term': 'f-1', 'label': CATEGORY_LABLE_F + u'即時新聞', 'scheme': URL_FOCUSES + '?category=1'},
  {'term': 'f-4', 'label': CATEGORY_LABLE_F + u'懶人包', 'scheme': URL_FOCUSES + '?category=4'},
  {'term': 'f-3', 'label': CATEGORY_LABLE_F + u'阿草觀點', 'scheme': URL_FOCUSES + '?category=3'},
  {'term': 'f-2', 'label': CATEGORY_LABLE_F + u'影音圖輯', 'scheme': URL_FOCUSES + '?category=2'},
  {'term': 'v-0', 'label': CATEGORY_LABLE_V + u'好球', 'scheme': URL_VIDEO + '?category=0'},
  {'term': 'v-1', 'label': CATEGORY_LABLE_V + u'烏龍球', 'scheme': URL_VIDEO + '?category=1'},
  {'term': 'v-2', 'label': CATEGORY_LABLE_V + u'界外球', 'scheme': URL_VIDEO + '?category=2'},
  {'term': 'v-3', 'label': CATEGORY_LABLE_V + u'重要現場', 'scheme': URL_VIDEO + '?category=3'}]

# FEED
FEED_TITLE = u'沃草國會無雙'
FEED_SUBTITLE = u'國會無雙是沃草的第一個產品，本公司致力於提供公民更好的參與時政的空間、工具與平台。公民應該監督立法院與民意代表， \
    因為我們都有能讓國家更好的權利，而我們應該為了自己、也為了自己珍惜的理念和人們，行使我們的權力。'
FEED_AUTHOR = {'name': u'沃草', 'email': 'musou@watchout.tw'}
FEED_LOGO = 'https://feed.musou.tw/static/images/nav-musou-212.png'

# Full Content List
# EX : [{'name':'test','token':'486e340013ddb40edf00ee3bfa6b601e9cfe05093ffec68cda58279de3f4d6c1'}]
TOKEN_LIST = []

# bunko 
BUNKO_URL = 'https://watchout.tw/feed.json'