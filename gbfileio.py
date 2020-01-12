VERSION_NUMBER = 0

def get_type_string(typ):
    if typ == "game":
        typestring="GAME BAKER"
    elif typ == "sprite":
        typestring="GAME BAKER SPRITE"
    elif typ == "savegame":
        typestring="GAME BAKER SAVEGAME"
    elif typ == "workstate":
        typestring="GAME BAKER WORKSTATE"
    return typestring


def savegame(filename,game,method="yaml",typ="game"):
    s = ""
    if method == "yaml":
        s = makeyaml(game)
    elif method == "pickle":
        s = makepickle(game)

    s = s.replace("\\","\\\\")

    f = open(filename, "w")

    typestring = get_type_string(typ)

    filestring = """#!/usr/bin/env python
# LEAVE THE FOLLOWING TWO LINES
# %s
# %s
# %d
s = \"\"\"
%s
\"\"\"
if __name__ == \"__main__\":
  import gbfileio,sys,runtime
  game = gbfileio.loadgame(sys.argv[0])
  runtime.run_game(game)
"""%(typestring,method,VERSION_NUMBER,s)

    f.write(filestring)
    f.close()

def loadgame(filename,typ="game"):

    typestring = get_type_string(typ)

    f = open(filename, "r")
    data = f.read()
    f.close()

    lines = data.splitlines()
    if lines[2] == "# %s"%(typestring,):
        method = lines[3][2:]
        version = int(lines[4][2:])
    else:
        raise Exception()

    s = "\n".join(lines[6:-5])

    s = s.replace("\\\\","\\")

    if method == "yaml":
        game = unyaml(s)
    elif method == "pickle":
        game = unpickle(s)

    return game
    


def unyaml(s):
    import yaml
    game = yaml.load(s)
    return game

def makeyaml(game):
    import yaml
    s=yaml.dump(game)
    return s

def makepickle(game):
    s = ""
    try:
        import cPickle
        s = cPickle.dumps(game)
    except:
        import pickle
        s = pickle.dumps(game)
    return s

def unpickle(s):
    try:
        import cPickle
        game = cPickle.loads(s)
    except:
        import pickle
        game = pickle.loads(s)
    return game
