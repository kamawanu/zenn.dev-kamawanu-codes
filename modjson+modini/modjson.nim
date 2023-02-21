import json,strutils,os,tables,strformat

type
    jsondoc = ref object
        fn: string
        tree: JsonNode

proc makepos(key:string) :  seq[string] =
    return key.split(".")

proc dig(src:jsondoc,key:string) : JsonNode =
    let pos = key.makepos()
    var parent: JsonNode = src.tree
    for key1 in pos:
        assert parent.kind == JObject and parent.fields.hasKey(key1), fmt"not in object tree <{key1}>"
        parent = parent.fields[key1]
    return parent

proc setvalue(root:jsondoc, keystr: string, val:string ) =
    let key = makepos(keystr)
    var parent = root.tree
    for kk in key[0..^2]:
        if not parent.haskey(kk):
            parent.add(kk,newJObject())
        parent = parent.fields[kk]
    let lastkey = key[^1]
    parent[lastkey] =
        if parent.hasKey(lastkey) and parent[lastkey].kind == JInt:
            newJInt(parseInt(val))
        elif not parent.hasKey(lastkey):
            try:
                newJInt(parseInt(val))
            except:
                newJString(val)
        else:
            newJString(val)

proc safejsonloader(fn:string) : jsondoc =
    let tree = json.parseJson(open(fn,fmRead).readAll())
    return jsondoc(tree:tree,fn:fn)

proc getvalue(src:jsondoc,key:string) : JsonNode =
    let pos = src.dig(key)
    return pos

proc jsonwriter(src:jsondoc,fo:File) =
    let root:JsonNode = src.tree
    fo.write($root)
    fo.close()

proc jsonwriter(src:jsondoc) =
    src.jsonwriter(open(src.fn,fmWrite))

var storage: jsondoc

for arg1 in os.commandLineParams():
    let maybekv = arg1.split("=",2)
    if arg1.existsFile():
        storage = safejsonloader(arg1)
        #echo repr(chunk)
    elif arg1[0] == '=':
        let ns = arg1[1..^1]
        assert storage != nil,"data not loaded."
        echo storage.getvalue(ns)
    elif maybekv.len == 2 and maybekv[0].len >= 1 and maybekv[1].len >= 1:
        assert storage != nil,"data not loaded."
        storage.setvalue(maybekv[0],maybekv[1])
    elif arg1 == "/":
        assert storage != nil,"data not loaded."
        storage.jsonwriter()
    elif arg1 == "/-":
        assert storage != nil,"data not loaded"
        storage.jsonwriter(stdout)
