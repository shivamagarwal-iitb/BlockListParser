from BlockListParser import BlockListParser
import time, sys

privacy_list = "../../blacklists/easyprivacy.txt"
ad_list = "../../blacklists/easylist.txt"

creator = BlockListParser(ad_list)

url = sys.argv[1]
print creator.should_block_and_print(url)
print creator.should_block_with_items(url)
