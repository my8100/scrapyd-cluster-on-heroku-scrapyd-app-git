# coding: utf-8
import io
import os
import re
from subprocess import Popen


# https://devcenter.heroku.com/articles/runtime-principles#web-servers
# The port to bind to is assigned by Heroku as the PORT environment variable.
PORT = os.environ['PORT']
NODE_NAME = os.environ.get('NODE_NAME', 'unset')
ENABLE_AUTH = os.environ.get('ENABLE_AUTH', 'True')
USERNAME = os.environ.get('USERNAME', '')
PASSWORD = os.environ.get('PASSWORD', '')
with io.open("scrapyd.conf", 'r+', encoding='utf-8') as f:
    f.read()
    f.write(u'\nhttp_port = %s\n' % PORT)
    if NODE_NAME != 'unset':
        f.write(u'\nnode_name = %s\n' % NODE_NAME)
    if ENABLE_AUTH == 'True':
        if USERNAME and PASSWORD:
            f.write(u'\nusername = %s\n' % USERNAME)
            f.write(u'\npassword = %s\n' % PASSWORD)


# Launch LogParser as a subprocess
logs_dir = '/app/logs'
if not os.path.exists(logs_dir):
    os.mkdir(logs_dir)

args = ['logparser', '-dir', logs_dir]
args.extend(['--scrapyd_server', '127.0.0.1:%s' % PORT])
args.extend(['--sleep', os.environ.get('PARSE_ROUND_INTERVAL', '10')])
if os.environ.get('ENABLE_TELNET', 'True') == 'False':
    args.extend(['--disable_telnet'])
if os.environ.get('VERBOSE', 'False') == 'True':
    args.extend(['--verbose'])
Popen(args)


# Specify the version of Scrapy
SCRAPY_VERSION = os.environ.get('SCRAPY_VERSION', '')
if re.search('^\d+\.\d+\.\d+$', SCRAPY_VERSION):
    os.system('pip install scrapy==%s' % SCRAPY_VERSION)
else:
    os.system('pip install scrapy')
