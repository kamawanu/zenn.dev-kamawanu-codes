# test_append_atomicity_indented_tabs.py
import os
import time
import random
from multiprocessing import Process

def worker(filename: str, lines: int, indent_tabs: int):
    """
    filename を O_APPEND モードで開き、
    プロセスごとに lines 行ずつランダムなタイミングで追記する。
    各行の先頭に indent_tabs 分タブ文字を入れてカラムをずらす。
    """
    fd = os.open(filename, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    pid = os.getpid()
    indent = "\t" * indent_tabs

    for i in range(lines):
        # ランダムに 0〜0.02 秒スリープしてタイミングをずらす
        time.sleep(random.random() * 0.02)
        line_text = f"{indent}PID {pid} - line {i}\n"
        os.write(fd, line_text.encode())

    os.close(fd)

if __name__ == "__main__":
    logfile = "test.log"

    # 既存ファイルがあれば削除
    try:
        os.remove(logfile)
    except FileNotFoundError:
        pass

    procs = []
    num_procs = 5
    lines_per_proc = 10
    indent_unit = 2  # プロセスごとに何タブずらすか

    for idx in range(num_procs):
        indent_tabs = idx * indent_unit
        p = Process(target=worker, args=(logfile, lines_per_proc, indent_tabs))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

    # 書き込まれた内容を表示
    print("=== test.log の中身 ===")
    with open(logfile, "r") as f:
        print(f.read())
