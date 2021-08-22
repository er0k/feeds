#!/usr/bin/env python3

import argparse
import feedparser
import PyRSS2Gen
import toml
from datetime import datetime
from db import feeds_db
from time import mktime


parser = argparse.ArgumentParser(description='Make a feed from other feeds')
parser.add_argument(
    '-c',
    '--config-file',
    help='Config file. default: feeds.toml',
    default='feeds.toml'
)
args = parser.parse_args()
conf = toml.load(args.config_file)
fdb = feeds_db(conf['db_file'])

for name, url in conf['feeds'].items():
    print(f"fetching {name} ({url})...")
    feedparser.USER_AGENT = conf['user_agent']
    parsed_feed = feedparser.parse(url)

    for entry in parsed_feed['entries']:
        fdb.insert_entry(
            name,
            entry['title'],
            entry['description'],
            entry['link'],
            entry['guid'],
            datetime.fromtimestamp(mktime(entry['published_parsed']))
        )


items = []
for entry in fdb.get_entries():
    if not entry['isdeleted']:
        items.append(PyRSS2Gen.RSSItem(
            title=f"{entry['service']} :: {entry['title']}",
            description=entry['description'],
            link=entry['link'],
            guid=entry['guid'],
            pubDate=entry['pub_date']
        ))

rss = PyRSS2Gen.RSS2(
    title=conf['title'],
    link=conf['link'],
    description=conf['description'],
    lastBuildDate=datetime.now(),
    items=items
)

rss.write_xml(open(conf['out_file'], 'w'))
