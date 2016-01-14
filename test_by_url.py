from BlockListParser import BlockListParser
import time, sys

privacy_list = "../../easyprivacy.txt"
ad_list = "../../easylist.txt"

with open(ad_list) as f:
    regex_lines = f.readlines()
creator = BlockListParser(regex_lines)

url = sys.argv[1]
print creator.should_block_and_print(url)
