import strutils,os

type
    inidepth = tuple
        sec:string
        key:string
        #value:string

    iniline = ref object
        raw:string
        pos:inidepth
        value:string

    inidocument = ref object
        fn: string
        ln: seq[iniline]

    kv = tuple
        k:string
        v:string

proc todepth(key:string) : inidepth =
    let pos = key.split(".")
    result = if pos.len == 1:
            ( "", pos[0] )
        else:
            ( pos[0],pos[1])

proc findkey(src:inidocument,pos:inidepth) : int =
    result = -1
    for ii in 0..(src.ln.len-1):
        if src.ln[ii].pos == pos:
            return ii


proc getvalue(src:inidocument,key:string) : string =
    let ii = src.findkey(key.todepth())
    result = ""
    if ii >= 0:
        result = src.ln[ii].value

proc setvalue(src:inidocument,key:string,value:string) =
    let pos:inidepth = key.todepth()
    var ii = src.findkey(pos)
    if ii < 0:
        var secpos = (pos.sec,"")
        ii = src.findkey(secpos)+1
        assert ii != 0, "undefined section"
        src.ln.insert(iniline(),ii)
    src.ln[ii].pos = (pos.sec,pos.key)
    src.ln[ii].raw = pos.key & "=" & value
    src.ln[ii].value = value

proc iniwriter(src:inidocument,fo:File) =
    for ln1 in src.ln:
        fo.write(ln1.raw & "\n")
    fo.close()

proc iniwriter(src:inidocument) =
    src.iniwriter(open(src.fn,fmWrite))

proc safeiniloader(fn:string) : inidocument =
    ## 標準のparsecfgはかなり挙動がデリケートなので自作
    ## 空行は残したい
    result = inidocument()
    let fo : File = open(fn,fmRead)
    var section:string = ""
    while not fo.endOfFile():
        let buf : string = fo.readLine().strip()
        var maybekv : kv = ("","")
        if buf.len == 0 or buf[0] == '#':
            discard
        elif buf.len > 2 and buf[0] == '[' and buf[^1] == ']':
            section = buf[1..^2]
            ###maybekv = ("","")
        else:
            var kvp = buf.split("=",2)
            if kvp.len == 2 and kvp[0].len > 0:
                #if ( kvp[1][0] == '"' or kvp[1][0] == '\'' ) and kvp[1][^1] == kvp[1][0]:
                #    kvp[1] = kvp[1][1..^2]
                maybekv = (kvp[0],kvp[1])
        let chunk : iniline = iniline(raw:buf,pos:(section,maybekv.k),value:maybekv.v)
        result.ln.add(chunk)
    result.fn = fn

var storage : inidocument
for arg1 in os.commandLineParams():
    let maybekv:seq[string] = arg1.split("=",2)
    if arg1.existsFile():
        storage = safeiniloader(arg1)
    elif arg1[0] == '=':
        var ns = arg1[1..^1]
        assert storage != nil,"data not loaded."
        echo storage.getvalue(ns)
    elif maybekv.len == 2 and maybekv[0].len >= 1:
        assert storage != nil,"data not loaded."
        storage.setvalue(maybekv[0],maybekv[1])
    elif arg1 == "/":
        assert storage != nil,"data not loaded."
        storage.iniwriter()
    elif arg1 == "/-":
        assert storage != nil,"data not loaded"
        storage.iniwriter(stdout)
