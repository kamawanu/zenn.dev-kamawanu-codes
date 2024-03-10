#!python3

from dataclasses import dataclass
from html.parser import HTMLParser
from typing import List, Dict


class finditeruser:
    def find(self, tag):
        try:
            return self.finditer(tag).__next__()
        except StopIteration:
            return None

    def findmust(self,tag):
        try:
            return self.finditer(tag).__next__()
        except StopIteration:
            raise TypeError(f"{self}.{tag} not found")


@dataclass
class htmldom(finditeruser):
    tag: str
    attrs: Dict[str, str]
    content: List["htmldom"]

    def __post_init__(self):
        if not type(self.attrs) is dict:
            self.attrs = dict(self.attrs)

    def __getitem__(self, ii):
        return self.content[ii]

    def finditer(self, tag):
        yield from finditerxi(self.content, tag)


def flatten(root: List[htmldom]):
    for xx in root:
        yield xx
        if isinstance(xx, htmldom):
            yield from flatten(xx.content)


def finditerxi(root: List[htmldom], tag):
    for xx in flatten(root):
        if isinstance(xx, htmldom) and xx.tag == tag:
            yield xx


class tinyhtmlparser(HTMLParser,finditeruser):
    root: List[htmldom] = None
    _nest: List[List[htmldom]] = None

    def __init__(self):
        self.root = list()
        self._nest = [self.root,]
        super().__init__()

    def finditer(self, tag):
        yield from finditerxi(self.root, tag)

    lonelytags = ("meta","link","img")

    def handle_starttag(self, tag, attrs):
        if tag in self.lonelytags:
            if len(self._nest) > 2 and self._nest[-2][-1].tag in self.lonelytags:
                self._nest.pop()
        # breakpoint()
        self._nest[-1].append(htmldom(tag, attrs, list()))
        self._nest.append(self._nest[-1][-1].content)

    def handle_endtag(self, tag):
        while tag != self._nest[-2][-1].tag:
            self._nest.pop()
        assert tag == self._nest[-2][-1].tag
        self._nest.pop()

    def handle_data(self, data):
        self._nest[-1].append(data)


htmlminiparser = tinyhtmlparser

def from_string(src:str) -> tinyhtmlparser:
    ob = tinyhtmlparser()
    ob.feed(src)
    return ob

if __name__ == "__main__":
    import glob
    for fn in glob.glob("*.html"):
        rawhtmlstr = open(fn).read()
        pz = from_string(rawhtmlstr)
        # ppr = pprint.PrettyPrinter(indent=1)
        # ppr.pprint(pz.root)
        print(pz.finditer("title").__next__().content)
