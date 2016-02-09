from BlockListParser import BlockListParser
import time, sys

privacy_list = "../../easyprivacy.txt"
ad_list = "../../easylist.txt"

creator = BlockListParser(ad_list)

url = sys.argv[1]
print creator.should_block_and_print(url)
