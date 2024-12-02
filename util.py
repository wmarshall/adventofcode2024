from pathlib import Path

TEST = Path(__file__).parent / 'test_inputs'
REAL = Path(__file__).parent / 'real_inputs'


def load_input(path: Path, day: int) -> str:
    return (path / str(day)).read_text()
