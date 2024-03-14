# Feeds Feed

Collect various RSS feeds and aggregate them to a single RSS feed

## Requirements

* python3

## Install

1. `python -m venv venv && . venv/bin/activate`

2. `pip install -r requirements.txt`

3. `cp feeds.toml.example feeds.toml`

## Run

`./feed.py`

This will:

- create the sqlite database and the `feeds` table if it does not already exist
- normalize each feed's publish date to UTC
- insert each feed entry in the database if it does not already exist
- create `feeds.rss` with all feed statuses, newest entries first

## Notes

- This does not do any caching. Each time it runs it will make new HTTP requests
to fetch feeds
