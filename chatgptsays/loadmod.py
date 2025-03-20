import importlib.util
import sys
import os


def load_module_from_file(file_path: str):
    """
    指定したファイルパスからモジュールを読み込み、モジュールインスタンスを返す関数です。

    Args:
        file_path (str): モジュールとして読み込む Python ファイルのパス。

    Returns:
        module: 読み込まれたモジュールのインスタンス。
    """
    # ファイル名（拡張子なし）を取得
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # モジュール名が数字で始まる場合、先頭にアンダースコアを付与する
    if base_name and base_name[0].isdigit():
        module_name = f"_{base_name}"
    else:
        module_name = base_name

    # specの作成
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"ファイル {file_path} からモジュールスペックを生成できませんでした")

    # モジュールインスタンスの生成
    module = importlib.util.module_from_spec(spec)

    # 他の場所からも参照できるようにsys.modulesに登録
    sys.modules[module_name] = module

    # モジュールの実行（読み込み）
    if spec.loader is None:
        raise ImportError(f"ファイル {file_path} のローダーが見つかりませんでした")
    spec.loader.exec_module(module)

    return module

# 使用例:
# module_instance = load_module_from_file('/path/to/1_module.py')
# module_instance.some_function()
