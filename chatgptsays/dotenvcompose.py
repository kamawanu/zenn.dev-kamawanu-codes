import sys
from typing import List, Dict, Optional

class EnvComposer:
    env_vars: Dict[str, str]

    def __init__(self) -> None:
        self.env_vars = {}

    def load_env_file(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    self.env_vars[key.strip()] = value.strip()

    def compose(self, file_paths: List[str]) -> None:
        for path in file_paths:
            self.load_env_file(path)

    def to_env_string(self) -> str:
        return '\n'.join(f'{key}={value}' for key, value in self.env_vars.items())

def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(1)
    composer: EnvComposer = EnvComposer()
    composer.compose(sys.argv[1:])
    print(composer.to_env_string())

if __name__ == '__main__':
    main()
