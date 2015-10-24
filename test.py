from BlockListParser import BlockListParser
import time, sys

privacy_list = "../../easyprivacy.txt"
ad_list = "../../easylist.txt"

with open(privacy_list) as f:
    regex_lines = f.readlines()
creator = BlockListParser(regex_lines)

with open('trialURLs') as f:
    urls = f.readlines()

options = {'script': True, 'domain': 'digitalspy.ca'}
print "********1*********"
print "url is http://www.qualtrics.com/f/metrics"
print creator.should_block("http://www.qualtrics.com/f/metrics")
print "********2*********"
print "url is http://www.cdnds.net/js/s_code.js"
print creator.should_block("http://www.cdnds.net/js/s_code.js", options)

# i = 0
# start = time.time()
# for url in urls:
#     creator.should_block(url, options)
#     i += 1
#     if i % 3000 == 0:
#         end = time.time()
#         print i, end - start
#         start = time.time()