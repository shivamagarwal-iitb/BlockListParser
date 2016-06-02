# BlockListParser
Code to detect if a url matches any of the regexes in lists like ad block plus lists

In order to use it,

  blocklist_parser = new BlockListParser(regex_file) 

or 

'''  
blocklist_parser = new BlockListParser(regexes)
'''

where regexes is comma separated list of regexes

Then to detect if something should be blocked,

blocklist_parser.should_block(ur, options)

where 
