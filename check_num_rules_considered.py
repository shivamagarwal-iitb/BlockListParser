from RegexParser import SingleRuleParser

options = {}
options["image"] = False
options["script"] = False
options["third-party"] = False
options["domain"] = ""

count_correct = 0
count_comment = 0
count_html = 0
total = 0

with open('../../blacklists/easylist.txt') as f:
    for regex_line in f:
        parser = SingleRuleParser(regex_line)
        result = parser.matching_supported(options)
        keys = parser.get_keys()
        is_comment = parser.get_comment()
        is_html_rule = parser.get_html_rule()
        if result:
            count_correct += 1
        elif is_comment:
            count_comment += 1
        elif is_html_rule:
            count_html += 1
        total += 1

print("Considered rules:", count_correct, count_correct*100.0/total, "%")
print("Comments:", count_comment, count_comment*100.0/total, "%")
print("HTML rules:", count_html, count_html*100.0/total, "%")
print("Rest remaining:", total - (count_correct + count_comment + count_html), (total - (count_correct + count_comment + count_html))*100.0/total, "%")
