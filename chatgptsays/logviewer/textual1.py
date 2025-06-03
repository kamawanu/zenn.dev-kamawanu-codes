import sys
from asyncio import sleep
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Static
from textual.reactive import reactive

class LogView(Static):
    log_lines = reactive([])

    def render(self):
        return "\n".join(self.log_lines)

class LogFilterApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    Input {
        dock: bottom;
    }
    """

    def __init__(self, log_path: str, **kwargs):
        super().__init__(**kwargs)
        self.log_path = log_path
        self.all_lines = []
        self.query = ""

    def compose(self) -> ComposeResult:
        self.log_view = LogView()
        yield self.log_view
        yield Input(placeholder="Filter keywords...")

    async def on_mount(self):
        try:
            with open(self.log_path, "r") as f:
                self.all_lines = f.readlines()
        except FileNotFoundError:
            self.all_lines = [f"ログファイルが見つかりません: {self.log_path}"]
        self.filter_and_update("")
        self.set_interval(0.5, lambda: None)  # イベントループ維持
        self.run_worker(self.watch_log, exclusive=True)

    async def watch_log(self):
        try:
            with open(self.log_path, "r") as f:
                f.seek(0, 2)  # ファイル末尾へ
                while True:
                    line = f.readline()
                    if line:
                        self.all_lines.append(line)
                        self.filter_and_update(self.query)
                    else:
                        await sleep(0.5)
        except Exception as e:
            self.all_lines.append(f"[読み取りエラー] {e}")
            self.filter_and_update(self.query)

    def on_input_changed(self, event: Input.Changed):
        self.query = event.value
        self.filter_and_update(self.query)

    def filter_and_update(self, query: str):
        keywords = query.lower().split()
        filtered = [
            line.rstrip()
            for line in self.all_lines
            if all(k in line.lower() for k in keywords)
        ]
        self.log_view.log_lines = filtered[-100:]  # 最新100行表示

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python logfilter.py /path/to/logfile.log")
        sys.exit(1)
    LogFilterApp(sys.argv[1]).run()
