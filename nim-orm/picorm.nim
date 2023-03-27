# This is just an example to get you started. A typical binary package
# uses this file as the main entry point of the application.

import typetraits, sequtils

#{.passC: "-d:nimCallDepthLimit=2".}

include "pico_orm.nim"

#proc `$`(src: VARCHAR): string {.borrow.}
#proc `$`(src: SMALLINT): string {.borrow.}
#proc `$`(src: BIGINT): string {.borrow.}
#proc `$`(src: INT): string {.borrow.}

when isMainModule:
  type
    playerData = object of ormmodel
      uid*: VARCHAR
      ap*: INT

  var c = dbconnect("localhost", "root", "root", "mysql")

  ####var data = ormquery[playerData](c, "SELECT * from playerData").toSeq()

  var datacontainer: orm1xnref[playerData];
  bulkload[playerData](datacontainer, c, "select * from playerData")

  var intvar1: int = 30

  for ii in 0..datacontainer.high:
    #var after = playerData(xx)
    datacontainer[ii].ap -= 30
    datacontainer[ii].ap = intvar1.INT
    datacontainer[ii].ap = (datacontainer[ii].ap - intvar1).INT

  for xx in toref(datacontainer):
    xx.ap += 30
    xx.ap = 9999.INT
    echo xx
    echo xx.getdiff()
