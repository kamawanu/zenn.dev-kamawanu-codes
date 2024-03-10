#!python3


from io import TextIOWrapper
from typing import Dict, List, Union, Optional
import re
from email.header import decode_header
import base64
import codecs
import os.path
from functools import lru_cache


class parametersets:
    """
    parameter sets
    """
    _src: str
    main: str
    modifiers: Dict[str, str]

    def __init__(self, value: str):

        def unquote(vv):
            if vv[0] == "\"" and vv[-1] == "\"":
                return vv[1:-1]
            return vv

        self._src = value
        self.main, *lst = re.split(r'\s*;\s*', value)
        self.modifiers = dict([
            (yy[0], unquote(yy[1]))
            for yy in
            [xx.split("=") for xx in lst]])

    def __str__(self):
        return self.main


class anypart:
    """
    discrete media
    """
    _rawheader: Dict[str, str]
    _rawbody: List[str]
    content_type: parametersets
    subject_decoded: str

    @lru_cache
    def _getbodysize(self):
        return sum([len(x) for x in self._rawbody])

    @property
    def bodysize(self):
        return self._getbodysize()

    def __init__(self, beheader: List[list]):
        # print(beheader)
        #dict(beheader)
        try:
          self._rawheader = dict([(xx[0].lower(), xx[1] ) for xx in beheader if len(xx) == 2 ])
        except IndexError as exc:
          print(beheader)
          raise exc
        self._rawbody = []
        # print(self.header)
        if "content-type" in self._rawheader:
            self.content_type = parametersets(
                self._rawheader["content-type"])
        if "subject" in self._rawheader:
            self.subject_decoded = subjectdecode(self._rawheader["subject"])

    def has_boundary(self)->Optional[str]:
        # assert "boundary" in self.header["content-type"].modifiers, self.header["content-type"].modifiers
        return self.content_type.modifiers["boundary"]

    @property
    def content_location(self) -> Optional[str]:
        return self._rawheader.get("content-location")

    def get_payload(self):
        # breakpoint()
        body = "\n".join(self._rawbody)
        encoding = self._rawheader["content-transfer-encoding"]
        if encoding == 'base64':
            body = base64.b64decode(body)
        elif encoding == 'quoted-printable':
            body = codecs.decode(body.encode("iso-8859-2"), 'quoted-printable').decode("utf-8", 'ignore')
        return body

    def get(self, name) -> Union[str,parametersets ,None]:
        return self._rawheader.get(name)


def subjectdecode(qp_subject_header: str) -> str:
    decoded_tuples = decode_header(qp_subject_header)
    decoded_str = ""

    has_charset=set([ x[1] for x in decoded_tuples if x[1] is not None ])

    for decoded_part in decoded_tuples:
        if decoded_part[1] is not None:
            decoded_str += decoded_part[0].decode(decoded_part[1],"ignore" )
        elif len(has_charset) > 0:
            decoded_str += decoded_part[0].decode(next(iter(has_charset)))
    return decoded_str


class multipartholder:
    """
    composite media
    """
    @property
    def toppart(self) -> anypart:
        return self.subparts[0]
    subparts: List[anypart]
    boundary = None
    _snapshotlocation = None
    _homefileptr = None

    def __init__(self):
        self.subparts = []
        # self.main = None

    def add(self, part: anypart):
        if len(self.subparts) == 0:
            self.boundary = part.has_boundary()
            self._snapshotlocation = part._rawheader["snapshot-content-location"]
        else:
            if self._snapshotlocation == part.content_location and self._homefileptr is None:
                self._homefileptr = len(self.subparts)
        self.subparts.append(part)

    @property
    def lastpart(self) -> anypart:
        if len(self.subparts) == 0:
            return self.toppart
        return self.subparts[-1]

    @property
    def homeurl(self) -> Optional[str] :
        return self._snapshotlocation

    def gethome(self) -> anypart:
        # breakpoint()
        if self._homefileptr is None:
          return None
        return self.subparts[self._homefileptr]

    @classmethod
    def from_file(cls, fn: Union[str,TextIOWrapper]) -> "multipartholder":
        if isinstance(fn,str):
            fp = open(fn)
        mparts = cls()
        pendingheaders: List[List[str, str]] = []
        boundary = None
        while buf := fp.readline():
            buf = buf.rstrip()
            if pendingheaders is not None:
                if buf == "":
                    # breakpoint()
                    mparts.add(
                        anypart(pendingheaders)
                    )
                    boundary = mparts.boundary
                    pendingheaders = None
                elif buf[0] in (" ", "\t"):
                    pendingheaders[-1][1] += " "
                    pendingheaders[-1][1] += buf[1:]
                else:
                    pendingheaders.append(buf.split(": "))
            elif buf == f"--{boundary}--":
                # breakpoint()
                break
            elif buf == f"--{boundary}":
                # breakpoint()
                pendingheaders = []
            else:
                mparts.lastpart._rawbody.append(buf)
        assert pendingheaders is None or pendingheaders == [], pendingheaders
        return mparts

def from_file(fn):
    return multipartholder.from_file(fn)

if __name__ == "__main__":
    import glob, sys
    lst = sys.argv[1:] or glob.glob("*.mht")
    mhtml = from_file(lst[0])
    # print(zzzz)
    # pprint.pprint(zzzz.parts)
    print(mhtml.toppart.subject_decoded)
    print(mhtml.toppart._rawheader["snapshot-content-location"])
    print([
        (xx.content_type.main) for xx in mhtml.subparts]
    )
    print(mhtml.gethome().get_payload())
    for yyy in mhtml.subparts:
        if yyy.content_type.main.split("/")[0] == "image":
            img = yyy.get_payload()
            ##breakpoint()
            if type(img) == bytes:
                open(os.path.basename(yyy.content_location), "wb").write(img)
