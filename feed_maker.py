 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import json
from bson import json_util
from instance import config
import MySQLdb
import datetime
import time
from pytz import timezone
import pytz
from feedgen.feed import FeedGenerator
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

twTime = timezone('Asia/Taipei')

# Settings
SITEURL = config.URL_SITEURL
FOCUSES_URL = config.URL_FOCUSES
VIDEO_URL = config.URL_VIDEO
PHOTOLINK = config.URL_PHOTOLINK
CATEGORY = config.CATEGORY

FEED_TITLE = config.FEED_TITLE
FEED_SUBTITLE = config.FEED_SUBTITLE
FEED_AUTHOR = config.FEED_AUTHOR
FEED_LOGO = config.FEED_LOGO


def make_rss(option):
    db = MySQLdb.connect(host=config.DB_HOST,    # your host, usually localhost
                        user=config.DB_USERNAME,         # your username
                        passwd=config.DB_PASSWORD,  # your password
                        db=config.DB_DATABASE,  # name of the data base
                        charset='utf8')
    cur = db.cursor()

    if option == 'FULL':
      cur.execute(config.DBEXECUTE_F)
    else:
      cur.execute(config.DBEXECUTE)
    db_data = cur.fetchall()
    db.close()

    fg = FeedGenerator()
    fg.id(SITEURL)
    fg.title(FEED_TITLE)
    fg.author({'name': FEED_AUTHOR['name'], 'email': FEED_AUTHOR['email']})
    fg.link(href=SITEURL, rel='alternate')
    fg.logo(FEED_LOGO)
    fg.subtitle(FEED_SUBTITLE)
    fg.link(href=SITEURL, rel='self')
    fg.language('zh-tw')

    for item in db_data:
        itemdata = pack_data(item, 'rss', option)
        fe = fg.add_entry()
        fe.id(itemdata['link'])
        fe.link(href=itemdata['link'], rel='alternate')
        fe.author(name=unicode(itemdata['author']), replace=True)
        fe.title(itemdata['title'])
        if option == 'FULL':
          fe.description(itemdata['abstract'])
          fe.content(content=itemdata['content'],type='CDATA')
        else:
          fe.description(itemdata['abstract'] + remore_link(itemdata['link']))
        fe.enclosure(url=itemdata['photo_thumb'], length=u'200', type=u'image/jpeg')
        fe.published(twTime.localize(itemdata['publish_date']))
        fe.category(category=get_category(itemdata['category']), replace=True)
    if option == 'FULL':
      fg.rss_file('rss_full.xml')
    else:
      fg.rss_file('rss.xml')


def make_live_json():
    db = MySQLdb.connect(host=config.DB_HOST,    # your host, usually localhost
                        user=config.DB_USERNAME,         # your username
                        passwd=config.DB_PASSWORD,  # your password
                        db=config.DB_DATABASE,  # name of the data base
                        charset='utf8')
    cur = db.cursor()
    cur.execute(config.DBEXECUTE_LIVE)
    datalist = cur.fetchall()
    db.close()
    data_dis = []
    for data in datalist:
      td = {'id':data[0],
            'title':unicode(data[1]),
            'photo_thumb':  unicode(config.URL_LIVEPHOTO + str(data[0]) + '/normal_' + data[2]),
            'link': config.URL_LIVE + str(data[0]),
            'state': data[3]}
      data_dis.append(td)

    with open('live.json', 'w') as fp:
      json.dump(data_dis, fp)
      fp.close()


def make_json(option):
    db = MySQLdb.connect(host=config.DB_HOST,    # your host, usually localhost
                        user=config.DB_USERNAME,         # your username
                        passwd=config.DB_PASSWORD,  # your password
                        db=config.DB_DATABASE,  # name of the data base
                        charset='utf8')
    cur = db.cursor()
    if option == 'FULL':
      cur.execute(config.DBEXECUTE_F)
    else:
      cur.execute(config.DBEXECUTE)
    datalist = cur.fetchall()
    db.close()

    data_dis = []
    for data in datalist:
      data_dis.append(pack_data(data, 'json', option))

    if option == 'FULL':
      make_linetoday(data_dis)
      with open('rss_full.json', 'w') as fp:
        json.dump(data_dis, fp)
        fp.close()
    else:
      with open('rss.json', 'w') as fp:
        json.dump(data_dis, fp)
        fp.close()


def make_linetoday(datalist):

  timenow = str(int(time.mktime(datetime.datetime.now().timetuple())))
  XMLHEAD = '<?xml version="1.0" encoding="UTF-8" ?><articles><UUID>watchoutmusou' + timenow + '000</UUID><time>' + timenow + '000' + '</time>'
  XMLFOOT = '</articles>'
  XMLARTICLE = ''
  for item in datalist:
    XMLARTICLE += '<article>'
    XMLARTICLE += '<ID>' + str(item['id']) + '</ID>'
    XMLARTICLE += '<nativeCountry>TW</nativeCountry><language>zh</language>'
    XMLARTICLE += '<startYmdtUnix>' + timenow + '000</startYmdtUnix>'
    XMLARTICLE += '<endYmdtUnix>1546300800000</endYmdtUnix>' # 2019/01/01
    XMLARTICLE += '<title>' + unicode(item['title']) + '</title>'
    XMLARTICLE += '<category>' + unicode(item['category']) + '</category>'
    XMLARTICLE += '<publishTimeUnix>' + str(item['publish_date']) + '000' + '</publishTimeUnix>'
    XMLARTICLE += '<contents>'
    XMLARTICLE += '<thumbnail><url>' + unicode(item['photo_thumb']) + '</url></thumbnail>'
    XMLARTICLE += '<text><content><![CDATA[' + unicode(item['content']) + ']]> </content></text>'
    XMLARTICLE += '</contents>'
    XMLARTICLE += '<author>' + unicode(item['author']) + '</author>'
    XMLARTICLE += '<sourceUrl>' + unicode(item['link']) + '</sourceUrl>'
    XMLARTICLE += '</article>'

  datapack = XMLHEAD + XMLARTICLE + XMLFOOT
  with open('linetoday.xml', 'w') as fp:
    fp.write(datapack)
    fp.close


def get_category(name):
    res = {'term': '0', 'label': u'沃草國會無雙', 'scheme': SITEURL}
    for item in CATEGORY:
      if item['label'] == name:
        res = item
    return res


def remore_link(link):
    return("<a href='" + link + "'>" + u"（閱讀全文⋯）" + "<a>")


def pack_data(data, ftype, option):

    data_item = ""
    d_link = ""
    d_category = ""
    d_publish_date = ""

    if ftype == 'json':
      d_publish_date = int(time.mktime(data[4].timetuple()))
    else:
      d_publish_date = data[4] + datetime.timedelta(hours=8)

    if data[7] == 'text':
      d_link = FOCUSES_URL + str(data[0])
      d_category = config.CATEGORY_LABLE_F + data[5]
    elif data[7] == 'video':
      d_category = config.CATEGORY_LABLE_V + data[8]
      d_link = VIDEO_URL + str(data[0])

    if data[3] is None:
      photo = ''
    else:
      photo = unicode(PHOTOLINK + str(data[0]) + '/normal_' + data[3])

    if option == 'FULL':
      data_item = {'id': int(data[0]),
        'title': data[1],
        'abstract': data[2],
        'photo_thumb': photo,
        'publish_date': d_publish_date,
        'category': d_category,
        'author': data[6],
        'link': d_link,
        'content':data[9]}
    else:
      data_item = {'id': int(data[0]),
        'title': data[1],
        'abstract': data[2],
        'photo_thumb': photo,
        'publish_date': d_publish_date,
        'category': d_category,
        'author': data[6],
        'link': d_link}

    return data_item


def write_log():

    t = datetime.datetime.now() + datetime.timedelta(hours=8)
    log = {'last_update_itme': str(t)}

    with open('log.json', 'w') as fp:
        json.dump(log, fp)
        fp.close()

if __name__ == "__main__":
    print '[System] Start! \n'
    make_rss('ABSTRACT')
    make_rss('FULL')
    print '[System] RSS Done!'
    make_json('ABSTRACT')
    make_json('FULL')
    print '[System] JSON Done!'
    make_live_json()
    print '[System] JSON Done!'
    # write_log()
    print '[System] LOG Done!'
