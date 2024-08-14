import PyInstaller.__main__
from pathlib import Path

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / "main.py")
path_to_statements = str(HERE / "statements")


def install():
    PyInstaller.__main__.run(
        [
            path_to_main,
            "--collect-submodules",
            "pyfuta",
            "--collect-submodules",
            "aiosqlite",
            "--add-data",
            f"{path_to_statements}/*:statements",
            "--onefile",
            # other pyinstaller options...
        ]
    )
