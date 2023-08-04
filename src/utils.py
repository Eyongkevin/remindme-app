from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def sort_dict(data: dict) -> dict:
    return {k: data[k] for k in sorted(data)}
