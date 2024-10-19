# main.py
from tasks import add
import time

def main():
    # タスクを非同期に実行
    result = add.delay(10, 20)
    print(f"Task ID: {result.id}")

    # タスクの結果を待つ
    while not result.ready():
        print("タスク実行中...")
        time.sleep(1)

    print(f"結果: {result.result}")

if __name__ == '__main__':
    main()
