from prompt_toolkit.shortcuts import input_dialog, message_dialog, button_dialog
import os, json, time, copy, sys
from datetime import datetime
from hashlib import sha256
from pathlib import Path

with open("config.json", "r") as r:
  config = json.load(r)
with open(config["directories"]["hashTemplate"], "r") as r:
  hashEntry = json.load(r)
hashEntry = copy.deepcopy(hashEntry)

def tobyte(inp):
  hexadecimal = None
  try:
    bytes.fromhex(inp)
    hexadecimal = True
  except:
    hexadecimal = False
  if isinstance(inp, int):
    return inp.to_bytes((inp.bit_length() + 7) // 8, "big")
  elif isinstance(inp, str) and hexadecimal == False:
    return inp.encode("utf-8")
  elif hexadecimal:
    return bytes.fromhex(inp)
  elif isinstance(inp, bool):
    return str(inp).encode("utf-8")
  elif inp is None:
    return str(inp).encode("utf-8")

def new(algo, source, hash, comment):
  hashEntry["metadata"]["timestamp"], hashEntry["entry"]["algo"], hashEntry["entry"]["source"], hashEntry["entry"]["hash"], hashEntry["comments"] = round(time.time()), algo, source, hash, comment
  if not os.path.exists(config["directories"]["hashEntries"]):
    hashEntry["metadata"]["prevHash"] = "0"*64
    db = [hashEntry]
  else:
    with open(config["directories"]["hashEntries"], "r") as r:
      db = json.load(r)
    hashEntry["metadata"]["prevHash"] = sha256(sha256(tobyte(db[-1]["metadata"]["prevHash"]) + tobyte(db[-1]["metadata"]["timestamp"]) + tobyte(db[-1]["metadata"]["index"]) + tobyte(db[-1]["entry"]["algo"]) + tobyte(db[-1]["entry"]["source"]) + tobyte(db[-1]["entry"]["hash"]) + tobyte(db[-1]["comments"])).digest()).hexdigest()
    hashEntry["metadata"]["index"] = len(db) + 1
    db.append(hashEntry)
  with open(config["directories"]["hashEntries"], "w") as w:
    if config["configs"]["compressed"]:
      json.dump(db, w, separators=(",", ":"))
    else:
      json.dump(db, w, indent=4)

def view(index):
  if not isinstance(index, int):
    return None
  else:
    with open(config["directories"]["hashEntries"], "r") as r:
      db = json.load(r)
    for entries in db:
      if entries.get("metadata", {}).get("index") == index:
        return f"{entries["metadata"]["index"]}<?>{entries["metadata"]["timestamp"]}<?>{entries["entry"]["hash"]}<?>{entries["entry"]["algo"]}<?>{entries["entry"]["source"]}<?>{entries["comments"]}"

def verify():
  if not os.path.exists(config["directories"]["hashEntries"]):
    return None
  else:
    with open(config["directories"]["hashEntries"], "r") as r:
      db = json.load(r)
    if len(db) == 1:
      if db[-1]["metadata"]["prevHash"] == "0"*64:
        return True
      else:
        return False
    else:
      for entries in range(1, len(db)):
        if sha256(sha256(tobyte(db[entries-1]["metadata"]["prevHash"]) + tobyte(db[entries-1]["metadata"]["timestamp"]) + tobyte(db[entries-1]["metadata"]["index"]) + tobyte(db[entries-1]["entry"]["algo"]) + tobyte(db[entries-1]["entry"]["source"]) + tobyte(db[entries-1]["entry"]["hash"]) + tobyte(db[entries-1]["comments"])).digest()).hexdigest() == db[entries]["metadata"]["prevHash"]:
          pass
        else:
          return False
      return True

def menu():
  val = verify()
  if val or val == None:
    pass
  else:
    message_dialog(title="Fatal Error", text=f"This Error is Due To Possible Tampering Detected In '{config["directories"]["hashEntries"]}'. Exiting in 3 Seconds.").run()
    time.sleep(3)
    sys.exit(1)
  moptions = button_dialog(title="HashCollector - Menu", text="Select An Option", buttons=[("New Hash", 1), ("View Hashes", 2), ("Settings", 3), ("Exit", 4)]).run()
  if moptions == 1:
    t = "HashCollector - New Hash"
    algo, source = input_dialog(title=t, text="What Hashing Algorithm is Used (Leave Blank If You Don't Know)").run(), input_dialog(title=t, text="Where Did This Hash Come From (Leave Blank If You Don't Know)").run()
    while True:
      hash = input_dialog(title=t, text="What Is The Hash (Required)").run()
      if hash == "":
        message_dialog(title=t, text="Error - Must Include A Hash").run()
        time.sleep(1)
      else:
        break
    comments = input_dialog(title=t, text="Optional Comments (Leave Blank If Needed)").run()
    if algo == "":
      algo = "unknown"
    if source == "":
      source = "unknown"
    if comments == "":
      comments = None
    new(algo, source, hash, comments)
    message_dialog(title=t, text="New Hash Imported!").run()
    time.sleep(1)
    menu()
  elif moptions == 2:
    t = "HashCollector - View Hashes"
    if not os.path.exists(config["directories"]["hashEntries"]):
      message_dialog(title=t, text="No Existing Hashes Yet.").run()
      time.sleep(1)
      menu()
    else:
      with open(config["directories"]["hashEntries"], "r") as r:
        db = json.load(r)
      indexes = []
      for entries in db:
        indexes.append((f"Hash #{str(entries.get("metadata", {}).get("index"))}", entries.get("metadata", {}).get("index")))
      indexes.append(("Exit", "exit"))
      allHashes = button_dialog(title=t, text="Select Hash Index To View", buttons=indexes).run()
      if allHashes == "exit":
        menu()
      else:
        index, timestamp, hash, algo, source, comment = view(allHashes).split("<?>")
        message_dialog(title=t, text=f"Hash Index: {index}\nDate: {datetime.fromtimestamp(timestamp)}\n---\nHash: {hash}\nAlgorithm: {algo}\nSource: {source}\n---\nComments: {comment}").run()
        menu()
  elif moptions == 3:
    t = "HashCollector - Settings"
    soptions = button_dialog(title=t, text=None, buttons=[("Data Compression", 1), ("Information", 2), ("Exit", 3)]).run()
    if soptions == 1:
      if config["configs"]["compressed"]:
        soption = button_dialog(title=t, text="Do You Want To Disable DB Compression?", buttons=[("Yes", 1), ("No", 2)]).run()
        if soption == 1:
          config["configs"]["compressed"] = False
          with open("config.json", "w") as w:
            json.dump(config, w, indent=4)
        else:
          menu()
      elif config["configs"]["compressed"] == False:
        soption = button_dialog(title=t, text="Do You Want To Enable DB Compression?", buttons=[("Yes", 1), ("No", 2)]).run()
        if soption == 1:
          config["configs"]["compressed"] = True
          with open("config.json", "w") as w:
            json.dump(config, w, indent=4)
        else:
          menu()
    elif soptions == 2:
      message_dialog(title=t, text=f"Version: {str(config["metadata"]["version"])}\nDeveloper: {config["metadata"]["developer"]}\nGithub: {config["metadata"]["github"]}\nCreated: {datetime.fromtimestamp(config["metadata"]["created"])}").run()
      menu()
  elif moptions == 4:
    sys.exit(0)

menu()
