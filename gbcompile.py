"""Functions to compile a game-baker game"""


def compile_to_python_PICKLE(game,filename="out.py",shebang="/usr/bin/env python"):
    pass

def compile_to_python(game,filename="out.py",shebang="/usr/bin/env python"):
    """Creates a "stand-alone" python game - still need to distribute
       game.py and runtime.py with the script (plus images etc).

       format is:

       == imports ==
       == pickled game instance ==

       == function to unpickle instance and run ==

       """

    pickled = ""



    """
    try:
        import gbfileio
        pickled = gbfileio.makeyaml(game)
    except:
        import pickle
        pickled = pickle.dumps(game)
    """
    import gbfileio
    pickled = gbfileio.makeyaml(game)
    pickled = pickled.replace("\\","\\\\")

    gamecode = """#!%s 



# Import Game-Baker libraries
from runtime import *
from game import *

# Pickled Game-Baker Game
gamepickle = \"\"\"%s\"\"\"

if __name__ == "__main__":
    # Unpickle the game
    game = None
    try:
        import yaml
        game = yaml.load(gamepickle)
    
    except:
        import pickle
        game = pickle.loads(gamepickle)

    # Try Running the Game
    run_game(game)
""" %(shebang,pickled)

    gamecode = """#!%s 



# Import Game-Baker libraries
from runtime import *
from game import *

# Pickled Game-Baker Game
gamepickle = \"\"\"%s\"\"\"

if __name__ == "__main__":
    # Unpickle the game
    game = None
    import yaml
    game = yaml.load(gamepickle)
    

    # Try Running the Game
    run_game(game)
""" %(shebang,pickled)


    # Save this to file
    out_file = open(filename, "w")
    out_file.write(gamecode)
    out_file.close()

    
