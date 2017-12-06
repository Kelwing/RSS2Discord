#!/usr/bin/env python

#    RSS2Discord
#    Copyright (C) 2017  Jacob Wiltse
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.



import argparse
import feedparser
import os
import re
import requests
import sys
import time
from models import *

db.connect()
db.create_tables([Link, Destination, Article, Feed], safe=True)

try:
    wh_url = os.environ['WEBHOOK_URL']
except:
    wh_url = None

def run(args):
    try:
        print('Starting the feed listener')
        while True:
            print('Checking feeds')
            feeds = Feed.select()
            for f in feeds:
                links = Link.select().where(Link.feed == f)
                d = feedparser.parse(f.url)
                if not f.initialized:
                    print(
                        f'Feed {f.id} is not initialized, adding all articles to database'
                    )
                for entry in d.entries:
                    if not f.initialized:
                        a = Article.create(
                            id=entry.id,
                            title=entry.title,
                            link=entry.link,
                            summary=entry.summary,
                            feed=f)
                    else:
                        try:
                            a = Article.get(Article.id == entry.id)
                        except:
                            # This is a new Article
                            print(
                                'Found new article, sending to linked webhooks'
                            )
                            summary = re.sub('<[^<]+?>', '', entry.summary)
                            title = re.sub('</?i>', '*', entry.title)
                            data = {
                                'username':
                                'TechNewsBot',
                                'content':
                                f'**{title}**\n{summary}\n[Read Article]({entry.link})'
                            }
                            a = Article.create(
                                id=entry.id,
                                title=entry.title,
                                link=entry.link,
                                summary=entry.summary,
                                feed=f)
                            for l in links:
                                requests.post(l.webhook.url, json=data)
                if not f.initialized:
                    print('Initialization done')
                    f.initialized = True
                    f.save()

            # Sleep for specified amount of time
            if args.runonce:
                sys.exit(0)
            time.sleep(args.freq)
        sys.exit(0)
    except Exception as e:
        print(f'Error in run: {e}')


def add_webhook(args):
    if wh_url and args.test:
        w = Destination.create(url=wh_url)
    else:
        w = Destination.create(url=args.url)
    print(f'Webhook added successfully with ID {w.id}')
    sys.exit(0)


def add_feed(args):
    f = Feed.create(url=args.url)
    print(f'Feed added successfully with ID {f.id}')
    sys.exit(0)


def rm_webhook(args):
    w = Destination.get(Destination.id == args.id)
    w.delete_instance()
    print(f'Webhook with ID {w.id} deleted successfully')
    sys.exit(0)


def rm_feed(args):
    f = Feed.get(Feed.id == args.id)
    f.delete_instance()
    print(f'Feed with ID {f.id} deleted successfully')
    sys.exit(0)


def list_webhook(args):
    webhooks = Destination.select()
    print('All registered webhooks:')
    for w in webhooks:
        print(f'{w.id}: {w.url}')
    sys.exit(0)


def list_feed(args):
    feeds = Feed.select()
    print('All registered feeds:')
    for f in feeds:
        print(f'{f.id}: {f.url}')
    sys.exit(0)


def list_link(args):
    links = Link.select()
    print('All feed to webhook links:')
    for l in links:
        print(f'{l.feed.id} => {l.webhook.id}')
    sys.exit(0)


def link(args):
    w = Destination.get(Destination.id == args.webhook)
    f = Feed.get(Feed.id == args.feed)
    l = Link.create(webhook=w, feed=f)
    print(f'Link created successfully with ID {l.id}')
    sys.exit(0)


parser = argparse.ArgumentParser(description='RSS to Discord Webhook')
subparsers = parser.add_subparsers(help='Command to run')

# Run command tree
parser_run = subparsers.add_parser('run', help='Run the RSS listener')
parser_run.add_argument(
    '--freq',
    type=int,
    action='store',
    default=600,
    help='Frequency (in minutes) to check the RSS feed')
parser_run.add_argument(
    '--runonce',
    action='store_true',
    help='Runs through the run function once, useful for running as a cron')
parser_run.set_defaults(func=run)

# Add command tree
parser_add = subparsers.add_parser(
    'add', help='Add a webhook or feed to the system')
add_sp = parser_add.add_subparsers(help='Add an item to the system')

parser_add_webhook = add_sp.add_parser(
    'webhook', help='Add a webhook to the system')
parser_add_webhook.add_argument(
    'url', help='Webhook URL to send new articles to')
parser_add_webhook.add_argument('--test', action='store_true', help='Loads a test webhook URL from the environment')
parser_add_feed = add_sp.add_parser('feed', help='Add a feed to the system')
parser_add_feed.add_argument('url', help='Feed URL to read articles from')
parser_add_webhook.set_defaults(func=add_webhook)
parser_add_feed.set_defaults(func=add_feed)

# Remove command tree
parser_rm = subparsers.add_parser(
    'rm', help='Remove a webhook or feed from the system')
rm_sp = parser_rm.add_subparsers(help='Remove an item from the system')

parser_rm_webhook = rm_sp.add_parser(
    'webhook', help='Remove a webhook from the system')
parser_rm_webhook.add_argument('id', help='ID of the webhook to remove')
parser_rm_feed = rm_sp.add_parser('feed', help='Remove a feed from the system')
parser_rm_feed.add_argument('id', help='ID of the feed to remove')
parser_rm_webhook.set_defaults(func=rm_webhook)
parser_rm_feed.set_defaults(func=rm_feed)

# List command tree
parser_list = subparsers.add_parser(
    'list', help='List all webhooks or feeds registered with the system.')
list_sp = parser_list.add_subparsers(
    help='List all webhooks or feeds registered with the system.')

parser_list_webhook = list_sp.add_parser(
    'webhook', help='List all webhooks registered with the system')
parser_list_feed = list_sp.add_parser(
    'feed', help='List all feeds registered with the system')
parser_list_link = list_sp.add_parser(
    'link', help='List all links registered with the system')
parser_list_webhook.set_defaults(func=list_webhook)
parser_list_feed.set_defaults(func=list_feed)
parser_list_link.set_defaults(func=list_link)

# Link command tree
parser_link = subparsers.add_parser('link', help='Link a feed to a webhook')

parser_link.add_argument('feed', help='ID of the feed you\'d like to link')
parser_link.add_argument(
    'webhook', help='ID of the webhook you\'d like to link')
parser_link.set_defaults(func=link)

args = parser.parse_args()
try:
    args.func(args)
except AttributeError as e:
    parser.print_help()
