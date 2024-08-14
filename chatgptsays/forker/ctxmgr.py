import os

class ForkAndWait:
    def __enter__(self):
        self.pid = os.fork()
        if self.pid == 0:
            # 子プロセスの場合
            return self
        else:
            # 親プロセスの場合は何も返さない
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        if self.pid == 0:
            # 子プロセスの場合
            os._exit(0)  # 子プロセスを終了
        else:
            # 親プロセスの場合
            os.waitpid(self.pid, 0)  # 子プロセスの終了を待機
            print(f"Child process {self.pid} finished")
