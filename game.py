"""game.py - game definition classes - these classes hold the entire
   game definition. All runtime data is NOT stored in instances of 
   these classes."""


class Game(object):
    """Base class for the representation of a Game"""
    def __init__(self,title):
        self.initcode=""
        self.objtype="Game"
        self.title = title
        self.gamescreens = {}
        self.workstates = {}
        self.gameobjects = {}
        self.sprites = {}
        self.startscreen = None

    def gamescreen(self,dimensions,name):
        """Use this to create a game-screen that is part of a game"""
        gs = GameScreen(dimensions)
        self.gamescreens[name] = gs
        return gs

    def gameobject(self,name):
        go = GameObject()
        go.name = name
        self.gameobjects[name] = go
        return go

    def workstate(self,name):
        ws = WorkState()
        self.workstates[name] = ws
        ws.actions[1] = """pass"""
        return ws

    def sprite(self,name):
        spr = Sprite(name)
        self.sprites[name] = spr
        return spr



class WorkState(object):
    """Class for a workstate (similar to usage of workflow in Zope/Plone)"""
    def __init__(self,inherits = None):
        self.objtype="Workstate"

        # Does the workstate inherit handlers?
        self.inherits = inherits

        #actions is a dict of events handlers.
        self.actions = {}


class GameScreen(object):
    """Class for an individual game-screen / scene / level"""
    def __init__(self,dimensions):
        self.objtype="Gamescreen"

        # list of objects that will be initially loaded
        self.startobjects = []
        self.dimensions = dimensions


class GameObject(object):
    """Class for a general object in a game"""
    def __init__(self):
        self.objtype="Gameobject"
        self.requires = [] # The Sprites that are required by this object
        self.baseworkstate = None # The Initial Work-state
        self.sprite = None
        self.x = 0
        self.y = 0
	

class Sprite(object):
    def __init__(self,name=""):
        self.objtype="Sprite"
        self.name=name
        # Store images in here.
        self.imagefiles = []
        self.alphakey = (255,255,255)
        self.framerate = 5
        pass
    def number_of_frames(self):
        return len(self.imagefiles)


