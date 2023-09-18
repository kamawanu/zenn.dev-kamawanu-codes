# Hello Nim!
import os
##import oswalkdir
import system
##import strutils
##import sequtils
import strformat
import posix
import times
import system/ansi_c
import segfaults
import terminal
###import sequtils
###let argc = paramCount()
let argv = commandLineParams()

var appname = paramStr(0)
####echo appname

let JENKINS_MODE = not terminal.isatty(stdin) or not terminal.isatty(stdout)
###let mypid = posix.getpid()

{.passL: "-static".}
{.passC:"-d:release"}
##{.passC:"-opt:size"}

proc writefl(f: File, a: varargs[string, `$`]) =
    for s in a: f.write s
    f.flushFile()

type
    nametuple = tuple
        dir: string
        name: string

type
    suspendException = object of CatchableError

proc raiser(a: cint) {.noconv.} =
    raise newException(suspendException, "message")

proc `$`(t: nametuple): string =
    return t.dir & "/" & t.name

proc tmp(t: nametuple): string =
    return t.dir & "/tmp"

ansi_c.c_signal(SIGTSTP, raiser)

var pri: cint = 10
discard posix.nice(pri)

proc ensure_readable(filename: string): bool =
    var data: posix.Stat
    var fn: cstring = filename
    var finfo = getFileInfo(filename)
    discard posix.stat(fn, data)

    var fp: FilePermission =
        if data.st_uid == posix.getuid():
            fpUserRead
        else:
            if data.st_gid == posix.getgid():
                fpGroupRead
            else:
                fpOthersRead;

    result = finfo.permissions.contains(fp)


proc safecopy1file(srcname: string, dst: nametuple) =
    let fileinfo: FileInfo = getFileInfo(srcname)
    ###echo fileinfo
    stdout.writefl "\"" & lastPathPart(srcname) & "\""
    ###stdout.flushFile()

    try:
        let beforetime = epochTime()

        assert ensure_readable(srcname)

        stdout.writefl fmt" {fileinfo.size} bytes "
        if JENKINS_MODE:
            stdout.writefl "\n"

        copyFile(srcname, dst.tmp)
        moveFile(dst.tmp, $dst)
        removeFile(srcname)

        let endtime = epochTime()
        let lapsetime = endtime - beforetime
        let speed = fileinfo.size.toBiggestFloat() / lapsetime

        stdout.writefl fmt" {speed:9.3f} bytes/s "

    except OSError:
        let exc: ref OSError = cast[ref OSError](getCurrentException())
        when defined(linux):
            case exc.errorCode
                of posix.ENAMETOOLONG:
                    echo "<" & exc.msg & ">"
                of posix.ENOSPC:
                    raise
                else:
                    echo repr(exc)
                    raise
        else:
            echo repr(exc)

    stdout.writefl ", "
    if JENKINS_MODE:
        stdout.writefl "\n"
    ###stdout.flushFile()
    return

proc tryRemoveDir(dir: string): void =
    var cfn: cstring = dir
    discard posix.rmdir(cfn)

proc dig(srcdir: string, dstdir: string) =
    stdout.writefl "[ \"", srcdir, "\" => \"", dstdir, "\" \t [ "
    if JENKINS_MODE:
        stdout.writefl "\n"
    ##stdout.flushFile()

    if not existsDir(dstdir):
        createDir(dstdir)
    assert srcdir.getFileInfo().kind == pcDir and dstdir.getFileInfo().kind == pcDir
    assert srcdir.getFileInfo().id != dstdir.getFileInfo().id, fmt"{srcdir} == {dstdir}"

    for ftype, bname in walkDir(srcdir, true):
        let srcname = srcdir & "/" & bname
        let dstname = dstdir & "/" & bname
        case ftype
        of pcDir:
            dig(srcname, dstname)
            tryRemoveDir(srcname)
        of pcFile:
            safecopy1file(srcname, (dstdir, bname))
        else:
            discard
        ##echo ftype,bname
    stdout.writefl "] ]\n"
    tryRemoveDir(srcdir)
    ##stdout.flushFile()

case argv.len:
    of 0, 1:
        echo appname & " <file|dir> ... <dir>"
    else:
        let dstdir = argv[argv.len-1]
        var leftargs: seq[TaintedString] = argv[0..argv.len-2]
        assert dstdir.dirExists() and not dstdir.fileExists()
        while len(leftargs) > 0:
            let anysrc = leftargs[0]
            leftargs.del(0)
            if anysrc[0] == '@':
                let tagfn = anysrc.substr(1)
                ###stdout.writefl(tagfn)
                let f = open(tagfn, FileMode.fmRead)
                defer:
                    close(f)
                while not f.endOfFile:
                    var ll = f.readLine()
                    leftargs.add(ll)
                continue
            let fileinfo: FileInfo = getFileInfo(anysrc)
            case fileinfo.kind
            of pcDir:
                dig(anysrc, dstdir)
            of pcFile:
                safecopy1file(anysrc, (dstdir, anysrc.lastPathPart()))
            else:
                discard
