import json, copy, sys, os, platform
from pathlib import Path

def localsave():
    if platform.system() == "Linux":
        os.makedirs(os.path.expanduser("~/.scutum"), exist_ok=True)
        return Path(os.path.expanduser("~/.scutum"))
    elif platform.system() == "Windows":
        os.makedirs(Path(os.environ["APPDATA"]) / "ScutumAuth", exist_ok=True)
        return Path(Path(os.environ["APPDATA"]) / "ScutumAuth")
    elif platform.system() == "Darwin":
        os.makedirs(Path(Path.home() / "Library" / "Application Support" / "ScutumAuth"), exist_ok=True)
        return Path(Path.home() / "Library" / "Application Support" / "ScutumAuth")

def unique():
    return os.urandom(16), os.urandom(12)

def template(path):
    with open(path, "r") as r:
        return copy.deepcopy(json.load(r))

def byte(txt):
    hexadecimal = False
    try:
        bytes.fromhex(txt)
        hexadecimal = True
    except:
        hexadecimal = False

    if isinstance(txt, int):
        return txt.to_bytes((txt.bit_length() + 7) // 8, "big")
    elif isinstance(txt, str) and hexadecimal == False:
        return txt.encode("utf-8")
    elif isinstance(txt, bool) or txt == None:
        return str(txt).encode("utf-8")
    elif isinstance(txt, list):
        if len(txt) == 0:
            return b""
        return json.dumps(txt).encode("utf-8")
    elif isinstance(txt, bytes):
        return txt
    elif hexadecimal:
        return bytes.fromhex(txt)

class absolute:
    def __init__(self, depth):
        self.depth = depth

    def dir(self, path):
        try:
            directory = Path(sys._MEIPASS)
        except:
            directory = Path(__file__).resolve().parents[self.depth]
        return directory / path
