import re


class RegexParser(object):
    def __init__(self):
        self.pattern = re.compile(
            r'<span .+></span>:<span .+>([\w_]+)</span>:</div>')

    def parse(self, text):
        return self.pattern.findall(text)
