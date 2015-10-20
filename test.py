from ShortcutMapCreator import ShortcutMapCreator
import time, sys

privacy_list = "../../../easyprivacy.txt"
ad_list = "../../../easylist.txt"

sizes = map(int, sys.argv[1].split(","))
creator = ShortcutMapCreator(sizes, privacy_list)
#creator.should_block("http://affiliates.swappernet.com")

with open('../trialURLs') as f:
    urls = f.readlines()

options = {'script': False, 'third-party': True, 'domain': 'www.foo.bar.mystartpage.com'}

i = 0
start = time.time()
for url in urls:
    creator.should_block(url, options)
    i += 1
    if i % 1000 == 0:
        end = time.time()
        print i, end - start
        start = time.time()