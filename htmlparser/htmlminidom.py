#!python3

from dataclasses import dataclass
from html.parser import HTMLParser
from typing import List, Dict


@dataclass
class dom:
    tag: str
    attrs: Dict[str, str]
    content: List["dom"]

    def __post_init__(self):
        if not type(self.attrs) is dict:
            self.attrs = dict(self.attrs)

    def __getitem__(self, ii):
        return self.content[ii]

    def finditer(self, tag):
        yield from finditerxi(self.content, tag)

    def find(self, tag):
        try:
          return self.finditer(tag).__next__()
        except StopIteration:
          return None

def flatten(root: List[dom]):
    for xx in root:
        yield xx
        if isinstance(xx, dom):
            yield from flatten(xx.content)


def finditerxi(root: List[dom], tag):
    for xx in flatten(root):
        if isinstance(xx, dom) and xx.tag == tag:
            yield xx


class htmlminiparser(HTMLParser):
    root: List[dom] = None
    _nest: List[List[dom]] = None

    def __init__(self):
        self.root = list()
        self._nest = [self.root,]
        super().__init__()

    def finditer(self, tag):
        yield from finditerxi(self.root, tag)

    def find(self, tag):
        try:
          return self.finditer(tag).__next__()
        except StopIteration:
          return None

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
