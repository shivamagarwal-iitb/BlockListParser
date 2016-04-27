
import re, pprint
from RegexParser import SingleRuleParser as srp

privacy_list = "../../easyprivacy.txt"
ad_list = "../../easylist.txt"

options_file = []
with open(privacy_list, "r") as f:
    for line in f:
        arr = re.split(r'\$+', line)
        if len(arr) > 1:
            options_file.append(arr[1].strip())

options_file.sort()

options_count = {}
for option in srp.BINARY_OPTIONS + ["domain"]:
    options_count[option] = sum(1 for regex in options_file if option in regex)


#for option in options:
 #   print option

pprint.pprint(options_count)