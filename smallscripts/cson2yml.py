#!python3

import glob
import cson # https://pypi.org/project/cson/
import os.path
import json
import os

foldersmap = dict([ 
    (z["key"],z["name"])
    for z in json.load(open("boostnoterepo/boostnote.json"))["folders"]
])

for fn in glob.glob("boostnoterepo/notes/*.cson"):
    try:
        y = cson.load(open(fn))
        # print(y["title"],y["content"])
        assert y["type"] == "MARKDOWN_NOTE"

        title = y["title"]
        if title == "" or len(title)>30:
            title = os.path.basename(fn)
        
        tags = y["tags"] + [ foldersmap[y["folder"]] , ]
        tagstr = ",".join(tags)

        mdo = open(f"bst-{title}.md", "w")
        mdo.write(f"title: {y['title']}\n")
        mdo.write(f"tags: {tagstr}\n")
        mdo.write("----\n")
        mdo.write(y["content"])
        mdo.close()
        os.remove(fn)
        #break
    except:
        pass
