import db_mysql, db_common, macros, json, parseutils, tables

type
    ormdb* = distinct DbConn
    ormdict* = distinct JsonNode
    VARCHAR* = string
    INT* = int32
    SMALLINT* = int16
    BIGINT* = int64

proc `+`*(x: INT, y: int): int = x.int + y

proc `-`*(x: INT, y: int): int = x.int - y

proc `+=`*(x: var INT, y: int|int32) =
    x = (x.int + y).INT

proc `-=`*(x: var INT, y: int|int32) =
    x = (x.int - y).INT


type
    ormmodel* = object of RootObj
        get_before_dict: ormdict

    orm1xn[T: ormmodel] = object
        rows: seq[T]

    orm1xnref*[T] = ref orm1xn[T]

proc newpico*(): ormdict =
    ormdict newJObject()

proc addint*(parent: ormdict, key, value: string) =
    var v: int = 0
    discard parseInt(value, v, 0)
    (JsonNode parent)[key] = % v

proc addstring*(parent: ormdict, key, value: string) =
    (JsonNode parent)[key] = % value

proc dbconnect*(spec, un, pw, dbn: string): ormdb =
    return ormdb db_mysql.open(spec, un, pw, dbn)

proc deserialize[T: ormmodel](src: ormdict): T =
    var xsrc: JsonNode = (JsonNode src).copy()
    xsrc["get_before_dict"] = newJNull()
    result = to[T](xsrc, T)
    result.get_before_dict = src

iterator rawquery*(conn: ormdb, query: string, args: varargs[
    string, `$`]): ormdict =
    var colspec: DbColumns
    for row1 in instantRows(DbConn conn, colspec, sql(query), args):
        var jsontree = newpico()
        for ii in 0..colspec.len-1:
            var nn = colspec[ii].name
            case colspec[ii].typ.kind
            of dbInt, dbUInt:
                jsontree.addint(nn, row1[ii])
            else:
                jsontree.addstring(nn, row1[ii])
        yield jsontree


proc high*[T: ormmodel](src: orm1xnref[T]): int =
    return src.rows.high()

proc `[]`*[T: ormmodel](src: orm1xnref[T], index: int): var T =
    return src.rows[index]

iterator ormquery*[T: ormmodel](conn: ormdb, query: string, args: varargs[
        string, `$`]): T =
    for raw1 in rawquery(conn, query, args):
        var ob = deserialize[T](raw1)
        yield ob

template bulkload*[T: ormmodel](pack: var orm1xnref[T], conn: ormdb,
    query: string, args: varargs[string, `$`]) =
    new pack
    pack.rows = ormquery[T](conn, query, args).toSeq()

iterator toref*[T: ormmodel](src: var orm1xnref[T]): var T =
    for ii in 0..src.rows.high:
        yield src.rows[ii]


proc `%`*[T: ormdict](child: T): JsonNode =
    result = newJNull()

proc toJson*[T: ormmodel](o: T): JsonNode =
    ## Construct JsonNode from tuples and objects.
    result = newJObject()
    for k, v in o.fieldPairs:
        if k != "get_before_dict":
            result[k] = %v

proc getdiff*[T: ormmodel](src: T): JsonNode =
    var before = JsonNode src.get_before_dict
    var after = src.toJson()
    result = newJObject()
    for k, v in after.pairs():
        if not before.contains(k) or before[k] != v:
            result.add(k, v)

