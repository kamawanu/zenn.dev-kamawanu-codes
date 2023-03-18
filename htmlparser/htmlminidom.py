#!python3

from dataclasses import dataclass
from html.parser import HTMLParser
from typing import List


@dataclass
class dom:
    tag: str
    attrs: dict
    content: List["dom"]


def flatten(root: List[dom]):
    for xx in root:
        yield xx
        yield from flatten(xx.content)


class htmlminiparser(HTMLParser):
    root: List[dom] = None
    _nest: List[List[dom]] = None

    def __init__(self):
        self.root = list()
        self._nest = [self.root,]
        super().__init__()

    def finditer(self, tag):
        for xx in flatten(self.root):
            if xx.tag == tag:
                yield xx

    def handle_starttag(self, tag, attrs):
        # breakpoint()
        self._nest[-1].append(dom(tag, attrs, list()))
        self._nest.append(self._nest[-1][-1].content)

    def handle_endtag(self, tag):
        # assert tag == self._nest[-1][-1].tag
        # breakpoint()
        self._nest.pop()

    def handle_data(self, data):
        self._nest[-1].append(data)


if __name__ == "__main__":
    import glob
    for fn in glob.glob("*.html"):
        rawhtmlstr = open(fn).read()
        pz = htmlminiparser()
        pz.feed(rawhtmlstr)
        # ppr = pprint.PrettyPrinter(indent=1)
        # ppr.pprint(pz.root)
        print(pz.finditer("title").__next__().content)
