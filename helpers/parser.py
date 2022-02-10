import re


class RegexParser(object):
    def __init__(self):
        self.pattern = re.compile(r":<span .+>([\w_]+)</span>:")

    def parse(self, text):
        return self.pattern.findall(text)
