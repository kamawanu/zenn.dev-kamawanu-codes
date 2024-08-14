import os
import functools


def fork_and_wait(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pid = os.fork()
        if pid == 0:
            # 子プロセスで関数を実行
            result = func(*args, **kwargs)
            os._exit(0)  # 子プロセスを終了
        else:
            # 親プロセスは子プロセスの終了を待機
            os.waitpid(pid, 0)
            print(f"Child process {pid} finished")
            return None  # 親プロセス側の戻り値は特に意味がないので None を返す

    return wrapper
