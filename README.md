# BlockListParser
Code to detect if a url matches any of the regexes in lists like ad block plus lists

In order to use it,

blocklist_parser = new BlockListParser(regex_file) 

or 

blocklist_parser = new BlockListParser(regexes)
where regexes is comma separated list of regexes

Then to detect if something should be blocked,

blocklist_parser.should_block(ur, options)
where options is a dictionary with keys like image, third-party, etc. (look at RegexParser.py for a list of options possible).

Also, use

blocklist_parser.should_block_with_items(url, options) 
to get the list of regexes which block a certain url
