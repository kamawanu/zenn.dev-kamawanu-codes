import yaml # https://nimyaml.org/index.html
#import yaml.serialization
#import dotenv
import json
#import parsecfg
import streams
import tables
#import parsecsv
import os
import strutils

proc add(root:JsonNode,key:string,value:string) =
  var f:int
  try:
    f = parseInt(value)
    root.add(key,newJInt(f))
  except:
    root.add(key,newJString(value))


proc add(root:JsonNode, key: seq[string], val:string ) =
  var parent = root
  ##var val = newJString(val)
  ##var key = okey
  for kk in key[0..^2]:
    if not parent.haskey(kk):
      parent.add(kk,newJObject())
      parent = parent.fields[kk]
  parent.add(key[^1],val)

proc tinyIniLoader(fn:string) : JsonNode =
  result = newJObject()
  var fo : File = open(fn,fmRead)
  var section:string = ""
  var parent = result
  while not fo.endOfFile():
    var buf : string = fo.readLine().strip()
    if buf.len == 0 or buf[0] == '#':
      continue
    if buf[0] == '[' and buf[-1] == ']':
      var ns :string = buf.substr(1,-1)
      if ns == section:
        continue
      if not result.fields.hasKey(ns):
        result.add(ns,newJObject())
      parent = result.fields[ns]
      section = ns
      continue
    var xx = buf.split("=",2)
    if xx[1].len >= 2 and xx[1][0] == '"' and xx[1][^1] == '\"':
      xx[1] = xx[1].substr(1,-1)
    parent.add(xx[0].split("."),xx[1])
    #echo $xx
    ##echo $parent


proc jyconvert(src:JsonNode) : YamlNode =
  ##result = newYamlNode(nil)
  case src.kind
  of JObject:
    var ttab : seq[(YamlNode,YamlNode)] = newSeq[(YamlNode,YamlNode)]()
    for xx in src.fields.pairs():
      var ee = jyconvert(xx[1])
      ##ee.tag = xx[0]
      ttab.add((newYamlNode(xx[0]),ee))
    var nt = newTable(ttab)
    return YamlNode(kind: yMapping, fields: nt )
  of JArray:
    var tseq : seq[YamlNode] = newSeq[YamlNode]()
    for x in src.elems:
      tseq.add(jyconvert(x))
    return newYamlNode(tseq)
  of JString:
    return newYamlNode(src.str)
  of JInt:
    return newYamlNode($src.num)
  of JFloat:
    return newYamlNode($src.fnum)
  of JBool:
    return newYamlNode($src.bval)
  of JNull:
    return newYamlNode("null")

proc ropen(fn:string) : File =
  if fn == "-":
    return stdin
  else:
    return open(fn)

proc wopen(fn:string) : File =
  if fn == "-":
    return stdout
  else:
    return open(fn,fmWrite)

var datum: JsonNode = nil
for arg1 in os.commandLineParams():
  var fn :string = arg1
  var arg1fs = arg1.splitFile()
  var tag:string = arg1fs.ext.substr(1)
  ##echo $tag,$arg1fs,$fn
  ##echo $arg1fs

  var hasop = arg1.split(":")
  if hasop.len > 1:
    fn = hasop[0]
    tag = hasop[1]
  ###echo $fn,$tag

  var isRead : bool = existsFile(fn)

  if isRead:
    #echo $tag
    case tag
    of "ini":
      datum = tinyIniLoader(fn)
    of "json":
      datum = json.parseJson(ropen(fn).readAll())
      #echo $datum
    of "yaml", "yml":
      var fstrm:Stream = ropen(fn).newFileStream()
      var qjs:seq[JsonNode] = yaml.loadToJson(fstrm)
      datum = newJArray()
      datum.elems.add(qjs)
      ###datum = newJArray(elems:nsq)
    ###echo $datum
  else:
    if datum != nil:
      case tag
      of "json":
        wopen(fn).write($datum)
      of "yaml":
        initYamlDoc(jyconvert(datum)).dumpDom(wopen(fn).newFileStream())
