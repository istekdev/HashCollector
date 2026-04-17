from components.toolbox import byte, localsave
import plyvel, time, os, json, re
from hashlib import sha256
from pathlib import Path

class database:
  def __init__(self, password):
    self.enc = aes(password)
    self.format = re.compile(r"^[A-Za-z0-9+/]{24}:\d+$")

  def new(self, hashingAlgo, source, hash):
    counter = 0
    for otherfiles in Path(localsave() / "bin" / "hashes").iterdir():
      checksum, index = otherfiles.name.split(":")
      if base64.b64encode(sha256(byte(hash)).digest()[:16]).decode() == checksum:
        return False
      if otherfiles.is_dir() and self.format.fullmatch(otherfiles.name):
        counter += 1

    dat = plyvel.DB(localsave() / "bin" / "hashes" / f"{base64.b64encode(sha256(byte(hash)).digest()[:16]).decode()}_{str(counter + 1)}", create_if_missing=False)
    dat.put(b"metadata:timestamp", byte(round(time.time())))
    dat.put(b"hashData:algo", byte(hashingAlgo))
    dat.put(b"hashData:source", byte(source))
    dat.put(b"hashData:hash", byte(hash))
    dat.close()
    return True

  def view(self, index):
    filename = None
    for otherfiles in Path(localsave() / "bin" / "hashes").iterdir():
      if otherfiles.name.split(":")[1] != index:
        return False
      filename = otherfiles.name
    if enc.verify() == False:
      return False

    dat = plyvel.DB(localsave() / "bin" / "hashes" / filename, create_if_missing=False)
    return bytearray(dat.get(b"metadata:timestamp")), bytearray(dat.get(b"hashData:algo")), bytearray(dat.get(b"hashData:source")), bytearray(dat.get(b"hashData:hash"))
