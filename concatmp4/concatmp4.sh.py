#!python3

import sys


def common_prefix(strs):
    if not strs:
        return ""

    prefix = strs[0]
    for string in strs[1:]:
        i = 0
        while i < len(prefix) and i < len(string) and prefix[i] == string[i]:
            i += 1
        prefix = prefix[:i]
    prefix = prefix + "X"

    return prefix


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("少なくとも1つ以上の文字列を入力してください。")
        sys.exit(1)

    strs = sys.argv[1:]
    result = common_prefix(strs)
    print(result)
