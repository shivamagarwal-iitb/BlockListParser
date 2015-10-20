import re, pprint
from FastHash import FastHash
from BlockListParser import BlockListParser

class ShortcutMapCreator:
    """Creates maps of shortcut hashes with regex of the urls"""

    def __init__(self, shortcut_sizes, block_list, support_hash = False):
        with open(block_list) as f:
            lines = f.readlines()
        self.fast_hashes = []
        self.support_hash = support_hash
        for shortcut_size in shortcut_sizes:
            self.fast_hashes.append(FastHash(shortcut_size))
        self.shortcut_sizes = shortcut_sizes
        self.all_shortcut_maps, self.remaining_lines = self._get_all_shortcut_maps(lines)
        self.all_shortcut_regex_maps = self._get_all_shortcut_regex_maps(self.all_shortcut_maps)
        self.remaining_regex = self._convert_to_regex(self.remaining_lines)

    def should_block(self, url, options=None):
        if self.support_hash:
            return self._should_block_with_hash()
        blacklisted = False
        for k in xrange(len(self.shortcut_sizes)):
            shortcut_size = self.shortcut_sizes[k]
            regex_map = self.all_shortcut_regex_maps[k]
            for i in xrange(len(url) - shortcut_size + 1):
                cur_sub = url[i:i+shortcut_size]
                if cur_sub in regex_map:
                    parser = regex_map[cur_sub]
                    if blacklisted:
                        if parser.is_whitelisted(url, options):
                            return False
                    else:
                        state = parser.check(url, options)
                        if state == 1:
                            return False
                        elif state == -1:
                            blacklisted = True
        if blacklisted:
            if self.remaining_regex.is_whitelisted(url, options):
                return False
        else:
            state = self.remaining_regex.check(url, options)
            if state == 1:
                return False
            elif state == -1:
                blacklisted = True
        return blacklisted

    def _convert_to_regex(self, lines):
        return BlockListParser(lines)

    def _should_block_with_hash(self, url, options):
        blacklisted = False
        for k in xrange(len(self.shortcut_sizes)):
            fast_hash = self.fast_hashes[k]
            shortcut_size = self.shortcut_sizes[k]
            regex_map = self.all_shortcut_regex_maps[k]
            prev_hash = -1
            for i in xrange(len(url) - shortcut_size + 1):
                cur_hash = fast_hash.extend_hash(url, i, prev_hash)
                if cur_hash in regex_map:
                    parser = regex_map[cur_hash]
                    if blacklisted:
                        if parser.is_whitelisted(url, options):
                            return False
                    else:
                        state = parser.check(url, options)
                        if state == 1:
                            return False
                        elif state == -1:
                            blacklisted = True
                prev_hash = cur_hash
        if blacklisted:
            if self.remaining_regex.is_whitelisted(url, options):
                return False
        else:
            state = self.remaining_regex.check(url, options)
            if state == 1:
                return False
            elif state == -1:
                blacklisted = True
        return blacklisted

    def _print_num_map(self, shortcut_map):
        num_shortcuts = {}
        num_shortcuts_stored = {}
        for shortcut in shortcut_map:
            num = len(shortcut_map[shortcut])
            if num in num_shortcuts:
                num_shortcuts[num] += 1
                num_shortcuts_stored[num].append(shortcut)
            else:
                num_shortcuts[num] = 1
                num_shortcuts_stored[num] = [shortcut]
        print num_shortcuts
        #pprint.pprint((num_shortcuts_stored))

    def _get_shortcut_map(self, pat, lines, shortcut_size):
        shortcut_map = {}
        secondary_lines = []
        total_rules = 0
        total_comments = 0
        total_shortcuts = 0
        for line in lines:
            line.strip()
            if line[0] == '!':
                total_comments += 1
                continue
            total_rules += 1
            url = re.split(r'\$+', line)[0]
            searches = pat.findall(url)
            flag = 0
            if searches:
                total_shortcuts += 1
            else:
                secondary_lines.append(line)
                continue
            min_count = -1
            for s in searches:
                for i in xrange(len(s) - shortcut_size+1):
                    cur_s = s[i:i+shortcut_size]
                    if cur_s not in shortcut_map:
                        shortcut_map[cur_s] = [line]
                        flag = 1
                        break
                    if min_count == -1 or len(shortcut_map[cur_s]) < min_count:
                        min_count = len(shortcut_map[cur_s])
                        min_s = cur_s
                if flag == 1:
                    break
            if flag == 0:
                shortcut_map[min_s].append(line)
        print "**********Shortcut size is %d**********" % shortcut_size
        print "Number of rules = ", total_rules, ", comments = ", total_comments
        print "Shortcuts found for ", total_shortcuts, " rules"
        print "Shortcuts not found for ", len(secondary_lines), " rules"
        print "Number map is"
        self._print_num_map(shortcut_map)
        return shortcut_map, secondary_lines

    def _get_all_shortcut_maps(self, lines):
        all_shortcut_maps = []
        for shortcut_size in self.shortcut_sizes:
            pat = re.compile(r'[\w\/\=\.\-\?\;\,\&]{%d,}' % shortcut_size)
            shortcut_map, lines = self._get_shortcut_map(pat, lines, shortcut_size)
            all_shortcut_maps.append(shortcut_map)
        return all_shortcut_maps, lines

    def _get_shortcut_regex_map(self, fast_hash, shortcut_map):
        shortcut_regex_map = {}
        if self.support_hash:
            for shortcut in shortcut_map:
                hash_value = fast_hash.compute_hash(shortcut)
                if hash_value in shortcut_regex_map:
                    shortcut_regex_map[hash_value].append(shortcut_map[shortcut])
                else:
                    shortcut_regex_map[hash_value] = shortcut_map[shortcut]
            for hash_key in shortcut_regex_map:
                shortcut_regex_map[hash_key] = self._convert_to_regex(shortcut_regex_map[hash_key])
        else:
            for shortcut in shortcut_map:
                shortcut_regex_map[shortcut] = self._convert_to_regex(shortcut_map[shortcut])
        return shortcut_regex_map

    def _get_all_shortcut_regex_maps(self, all_shortcut_maps):
        all_shortcut_regex_maps = []
        for fast_hash, shortcut_map in zip(self.fast_hashes, all_shortcut_maps):
            all_shortcut_regex_maps.append(self._get_shortcut_regex_map(fast_hash, shortcut_map))
        return all_shortcut_regex_maps