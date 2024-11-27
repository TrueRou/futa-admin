import PyInstaller.__main__
from pathlib import Path

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / "main.py")


def install():
    PyInstaller.__main__.run(
        [
            path_to_main,
            "--collect-submodules",
            "pyfuta",
            "--collect-submodules",
            "aiosqlite",
            "--onefile",
            # other pyinstaller options...
        ]
    )
