#!/usr/bin/env python

"""
Game Baker - Main Game Designer GUI

An open source, cross platform game design system
http://code.google.com/p/game-baker

Update 16 May 2008:

main class is MainGTK
- inherits event_connector and main_window_events

Basic layout is roughly MVC (model view controller)
- MainGTK contains is the Model
- main_view specifies the View
- main_window_events specifies the Controller

(of course, they are all one object through inheritance)

"""


#=imports=============================================

import sys,os
import runtime
import gobject
import game,GUI.treeview
from pygame.locals import *


from GUI.main_window_events import hide_window
from GUI.main_window_events import main_window_events


try:
     import pygtk
     pygtk.require("2.0")
except: pass

try:
    import gtk
    import gtk.glade
except: sys.exit(1)

#=END imports==========================================


def find_item_name(dic,item):
    a = [name for name in dic.keys() if dic[name] == item]
    if not len(a) == 1:
        return None
    else:
        return a[0]


class main_view():

    def set_view(self):
        """Sets up the GUI"""
        #Choose the glade file for the gui
        gladefile = os.path.join(self.gamebaker_location, "GUI" , \
                                        "gamebaker.glade" , "gamebaker.glade")

        self.wTree = gtk.glade.XML(gladefile)
        self.treeviewhelp = GUI.treeview.treeview_helper(self.wTree.get_widget("treeview1"))

        # Extra initialisation of combo boxes
        def init_combo_box(name):
        	cb = self.wTree.get_widget(name)
        	cell = gtk.CellRendererText()
        	cb.pack_start(cell,True)
        	cb.add_attribute(cell,'text',0)
        	
        init_combo_box("cbxworkstateevents")
        init_combo_box("cbx_workstateoptns")
        init_combo_box("cbx_gamescreen_object_options")

        # Set up the "initial objects" treeview
        treeview = self.wTree.get_widget("treeview_gamescreen_objects")
        column = gtk.TreeViewColumn("Name"
                    , gtk.CellRendererText(),
                    text=1) # position of column
        treeview.append_column(column)
        column = gtk.TreeViewColumn("Type"
                    , gtk.CellRendererText(),
                    text=2) # position of column
        treeview.append_column(column)


        # Connect specific events

        # Connect close button on dialog
        self.wTree.get_widget("aboutdialog1").connect("response",hide_window)




class MainGTK(main_window_events,main_view):
    """ Main Game Baker GUI class
        Event Handlers are inherited from main_window_events
        Connected from main_view
    """

    def __init__(self):
        #Location of game baker
        self.gamebaker_location = sys.path[0]

        # Load The GUI
        self.set_view()

        # Set up the Event Handlers
        self.connect_events()

        # Set up required vars
        self.game = None
        self.selectedworkstate=None
        self.filename = ""


    def add_game_object(self,name=None):
        if name is None:
            count = 1
            while self.game.gameobjects.has_key("GameObject%d"%count):
                count+=1
            name = "GameObject%d"%count
        mytestGameObject = self.game.gameobject(name)
        return mytestGameObject

    def add_workstate(self,name=None):
        if name is None:
            count = 1
            while self.game.workstates.has_key("Workstate%d"%count):
                count+=1
            name = "Workstate%d"%count
        mytestWorkState = self.game.workstate(name)
        return mytestWorkState

    def add_gamescreen(self,name=None,resolution=None):
        if name is None:
            count = 1
            while self.game.gamescreens.has_key("GameScreen%d"%count):
                count+=1
            name = "GameScreen%d"%count
        if resolution is None:
            resolution = (800,600)
        mytestGameScreen = self.game.gamescreen(resolution,name)

    def delete_gameobject(self,go):
        name = find_item_name(self.game.gameobjects,go)
        del self.game.gameobjects[name]
        # TODO Have to delete or warn about references
    
    def delete_sprite(self,sprite):
        name = find_item_name(self.game.sprites,sprite)
        del self.game.sprites[name]
        # TODO Have to delete or warn about references

    def delete_gamescreen(self,gs):
        name = find_item_name(self.game.gamescreens,gs)
        del self.game.gamescreens[name]
        # TODO Have to delete or warn about references

    def delete_workstate(self,workstate):
        name = find_item_name(self.game.workstates,workstate)
        del self.game.workstates[name]
        # TODO Have to delete or warn about references

    def run_game(self,widget = None):
        """Runs a game"""
        
        debug(self.game)
        #runtime.run_game(self.game)

    def import_external_sprite(self,filename):
        if not filename == "":
            import gbfileio
            newsprite = gbfileio.loadgame(filename,typ="sprite")
            name = ""
            try:
                name = newsprite.name
            except: pass
            if name == "":
                i = 1
                while self.game.sprites.has_key("ImportedSprite%d"%i):
                    i+=1
                name = "ImportedSprite%d"%i
            self.game.sprites[name] = newsprite


def debug(game):
    try:
        try:
            runtime.run_game(game)
        except runtime.gb_runtime_exception, inst:
            print inst
            msg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,buttons=gtk.BUTTONS_CLOSE)
            orig_str = str(inst.orig).replace("<","[").replace(">","]")
            orig_str = orig_str.replace("[string]", GUI.constants.event_names.get(inst.event,"Unknown") )
            workstate = inst.workstate
            if workstate is None:
                workstate = ""
            errormessage = """<b>Exception:</b> %s \n<b>Error:</b> %s \n<b>Event:</b>%s""" \
                            %(inst.log,orig_str,workstate + ":" + GUI.constants.event_names.get(inst.event,"Unknown") )

            def set_focus(widget,msg):
                """
                methinks the gtk.Window methods could do with some documentation strings

                (
                i.e. this is where we have to set the focus onto the msg Dialog - using a method
                inherited from gtk.Window - but this module seems completely undocumented in the
                docstrings and I'm nowhere near the internet right now :-(
                )
                """
                pass

            msg.connect("focus-out-event", set_focus )
            msg.set_markup(errormessage)
            msg.set_modal(True)
            result = msg.run()
            msg.destroy()
    except Exception, inst:
        print inst,str(inst)




if __name__ == "__main__":
    h = MainGTK()
    gtk.main()

