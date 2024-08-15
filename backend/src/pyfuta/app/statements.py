from pathlib import Path


def _read_file(filename: str, subfolder: str = ""):
    path1 = Path(__file__).parent.parent / "statements" / subfolder / f"{filename}"
    path2 = Path(__file__).parent.parent.parent / "statements" / subfolder / f"{filename}"
    if not path1.exists() and not path2.exists():
        raise FileNotFoundError(f"Statement file not found: {filename}.")
    path = path1 if path1.exists() else path2
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def SQL(filename: str):
    return _read_file(f"{filename}.sql")


def MIXIN(filename: str):
    return _read_file(f"{filename}.json", subfolder="mixins")
