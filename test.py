from BlockListParser import BlockListParser
import time, sys

privacy_list = "../../easyprivacy.txt"
ad_list = "../../easylist.txt"

with open(privacy_list) as f:
    regex_lines = f.readlines()
creator = BlockListParser(regex_lines)

with open('trialURLs') as f:
    urls = f.readlines()

options = {'script': False, 'third-party': True, 'domain': 'www.foo.bar.mystartpage.com'}

i = 0
start = time.time()
for url in urls:
    creator.should_block(url, options)
    i += 1
    if i % 3000 == 0:
        end = time.time()
        print i, end - start
        start = time.time()