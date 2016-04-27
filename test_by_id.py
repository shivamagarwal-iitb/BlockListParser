from BlockListParser import BlockListParser
import time, sys

from netlib.odict import ODictCaseless
from publicsuffix import PublicSuffixList
from urlparse import urlparse
import sqlite3

def fetchiter(cursor):
    """ Generator for cursor results """
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row

psl = PublicSuffixList()

# get options dict from url top_url and header of http response
def get_option_dict(url, top_url, header_str):
    options = {}
    options["image"] = False
    options["script"] = False
    options["third-party"] = False
    options["domain"] = ""

    image_types = ['tif', 'tiff', 'gif', 'jpeg', 'jpg', 'jif', 'jfif', 'jp2', 'jpx', 'j2k', 'j2c', 'fpx', 'pcd', 'png']
    script_types = ['js']
    # check if its an image
    header = ODictCaseless()
    header.load_state(eval(header_str))
    for content_type in header['Content-Type']:
        if "image/" in content_type:
            options["image"] = True
        if "javascript" in content_type:
            options["script"] = True

    extension = urlparse(url).path.split('.')[-1]
    if not options["image"] and extension in image_types:
        options["image"] = True
    if not options["script"] and extension in script_types:
        options["script"] = True
    top_hostname = urlparse(top_url).hostname
    hostname = urlparse(url).hostname
    top_domain = psl.get_public_suffix(top_hostname)
    domain = psl.get_public_suffix(hostname)
    if not top_domain == domain:
        options["third-party"] = True
    options["domain"] = top_hostname
    return options

privacy_list = "../../blacklists/easyprivacy.txt"
ad_list = "../../blacklists/easylist.txt"
ad_list5 = "../../blacklists/easylist_5.txt"
ad_list6 = "../../blacklists/easylist_6.txt"
use_list = privacy_list

db_path = "../../databases/2015-11_5k_ID_detection_1/2015-11_5k_ID_detection_1_census_crawl.sqlite"
table_name = "http_response_cookies_test_5k"
small_table_name = "http_response_cookies_test_small_5k"
use_table_name = small_table_name

creator = BlockListParser(use_list)

con = sqlite3.connect(db_path)
cur = con.cursor()
# Increase the cache size of the DB
# current size is 10GB
cur.execute("PRAGMA cache_size = -%i" % 10**7)
cur.execute("PRAGMA temp_store = 2") # Store temp tables, indicies in memory

ids = sys.argv[1]
id_list = ids.split()
for id in id_list:
    id = int(id)
    print("\n*****ID:", id)
    cur.execute("SELECT url, top_url, headers FROM %s WHERE id = %d" % (use_table_name, id))
    for url, top_url, header in fetchiter(cur):
        print("*****URL:", url)
        print("*****TOP_URL:", top_url)
        print("*****HEADER:", header)
        options = get_option_dict(url, top_url, header)
        print("*****OPTIONS:", options)
        print(creator.should_block_and_print(url, options))