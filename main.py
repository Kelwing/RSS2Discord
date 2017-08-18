import argparse
import feedparser
import sys
from models import *

def run(args):
    print('Starting the feed listener...')
    sys.exit(0)

def add_webhook(args):
    w = Destination.create(
            url=args.url
        )
    print(f'Webhook added successfully with ID {w.id}')

def add_feed(args):
    f = Feed.create(
            url=args.url
        )
    print(f'Feed added successfully with ID {f.id}')

def rm_webhook(args):
    w = Destination.get(
            Destination.id=args.id
        )
    w.delete_instance()
    print(f'Webhook with ID {w.id} deleted successfully')
    sys.exit(0)

def ls(args):

    sys.exit(0)

def link(args):
    pass

parser = argparse.ArgumentParser(description='RSS to Discord Webhook')
subparsers = parser.add_subparsers(help='Command to run')

# Run command tree
parser_run = subparsers.add_parser('run', help='Run the RSS listener')
parser_run.add_argument('--freq', type=int, action='store', help='Frequency (in minutes) to check the RSS feed')
parser_run.set_defaults(func=run)

# Add command tree
parser_add = subparsers.add_parser('add', help='Add a webhook or feed to the system')
add_sp = parser_add.add_subparsers(help='Add an item to the system')

parser_add_webhook = add_sp.add_parser('webhook', help='Add a webhook to the system')
parser_add_webhook.add_argument('url', help='Webhook URL to send new articles to')
parser_add_feed = add_sp.add_parser('feed', help='Add a feed to the system')
parser_add_feed.add_argument('url', help='Feed URL to read articles from')
parser_add_webhook.set_defaults(func=add_webhook)
parser_add_feed.set_defaults(func=add_feed)

# Remove command tree
parser_rm = subparsers.add_parser('rm', help='Remove a webhook or feed from the system')
rm_sp = parser_rm.add_subparsers(help='Remove an item from the system')

parser_rm_webhook = rm_sp.add_parser('webhook', help='Remove a webhook from the system')
parser_rm_webhook.add_argument('id', help='ID of the webhook to remove')
parser_rm_feed = rm_sp.add_parser('feed', help='Remove a feed from the system')
parser_rm_feed.add_argument('id', help='ID of the feed to remove')
parser_rm.set_defaults(func=rm)

# List command tree
parser_list = subparsers.add_parser('list', help='List all webhooks or feeds registered with the system.')
list_sp = parser_list.add_subparsers(help='List all webhooks or feeds registered with the system.')

parser_list_webhook = list_sp.add_parser('webhook', help='List all webhooks registered with the system')
parser_list_feed = list_sp.add_parser('feed', help='List all feeds registered with the system')
parser_list.set_defaults(func=ls)

# Link command tree
parser_link = subparsers.add_parser('link', help='Link a feed to a webhook')

parser_link.add_argument('feed', help='ID of the feed you\'d like to link')
parser_link.add_argument('webhook', help='ID of the webhook you\'d like to link')
parser_link.set_defaults(func=link)


args=parser.parse_args()
try:
    args.func(args)
except AttributeError as e:
    parser.print_help()

#d = feedparser.parse('https://www.theregister.co.uk/personal_tech/headlines.atom')
#for entry in d.entries:
#    print(f"ID: {entry.id}")
#    print(f"Title: {entry.title}")
#    print(f"Link: {entry.link}")
#    print(f"Summary: {entry.summary}")
#    print("\n--------------------")
