def getcaller(back=1):
    """
    stringized stackframe
    """
    import inspect
    top = inspect.stack()[-back]
    tag = f"({top.function}){top.filename}:{top.lineno}"
    return tag

def printcaller(func:callable = None,*,print=print):
    """
    decolator print stackframe
    """
    if func is None:
        del func
        def _2(func:callable):
            def _3(*args,**kwargs):
                print(getcaller())
                return func(*args,**kwargs)
            return _3
        return _2
    else:
        def _1(*args,**kwargs):
            print(getcaller())
            return func(*args,**kwargs)
        return _1

if __name__ == "__main__":
    ###breakpoint()
    import sys

    print(getcaller())

    @printcaller
    def func1():
        pass

    @printcaller(print=sys.stderr.write)
    def func2():
        pass

    func1()
    func2()
