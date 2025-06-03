# test_logging_atomicity_indented.py
import logging
import os
import time
import random
from multiprocessing import Process

def worker(filename: str, lines: int, indent_tabs: int):
    indent = "\t" * indent_tabs
    pid = os.getpid()

    logger = logging.getLogger(f"logger_{pid}")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename, mode='a', encoding='utf-8')
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    for i in range(lines):
        time.sleep(random.random() * 0.02)
        logger.info(f"{indent}PID {pid} - line {i}")

    handler.close()
    logger.removeHandler(handler)

if __name__ == "__main__":
    logfile = "test.log"

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
    with open(logfile, "r", encoding='utf-8') as f:
        print(f.read())
