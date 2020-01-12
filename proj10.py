######################################################################
#  Computer Project #10
#
#  Algorithm
#     The program allows the user to play Baker’s Game 
#     according to the rules 
#     The program will use the instructor supplied 
#     cards.py module to model the cards and deck of cards
#     The program will recognize valid commands  
#     and move card to targeted destination
#     The program will repeatedly display the current state of the game
#     and prompt the user to enter a command until the user wins the game 
#     or enters q, whichever comes first 
#     The program will detect, report, and recover from invalid commands
######################################################################
import cards #This is necessary for the project

BANNER = """
    __        _____ _   _ _   _ _____ ____  _ _ _ 
    \ \      / /_ _| \ | | \ | | ____|  _ \| | | |
     \ \ /\ / / | ||  \| |  \| |  _| | |_) | | | |
      \ V  V /  | || |\  | |\  | |___|  _ <|_|_|_|
       \_/\_/  |___|_| \_|_| \_|_____|_| \_(_|_|_)

"""


RULES = """
     ____        _             _        ____
    | __ )  __ _| | _____ _ __( )___   / ___| __ _ _ __ ___   ___
    |  _ \ / _` | |/ / _ \ '__|// __| | |  _ / _` | '_ ` _ \ / _ \\
    | |_) | (_| |   <  __/ |    \__ \ | |_| | (_| | | | | | |  __/
    |____/ \__,_|_|\_\___|_|    |___/  \____|\__,_|_| |_| |_|\___|

    Cells:       Cells are numbered 1 through 4. They can hold a
                 single card each.

    Foundations: Foundations are numbered 1 through 4. They are
                 built up by rank from Ace to King for each suit.
                 All cards must be in the foundations to win.

    Tableaus:    Tableaus are numbered 1 through 8. They are dealt
                 to at the start of the game from left to right
                 until all cards are dealt. Cards can be moved one
                 at a time from tableaus to cells, foundations, or
                 other tableaus. Tableaus are built down by rank
                 and cards must be of the same suit.

"""


MENU = """

    Game commands:
    
    TC x y    Move card from tableau x to cell y
    TF x y    Move card from tableau x to foundation y
    TT x y    Move card from tableau x to tableau y
    CF x y    Move card from cell x to foundation y
    CT x y    Move card from cell x to tableau y
    R         Restart the game with a re-shuffle
    H         Display this menu of commands
    Q         Quit the game
    
"""
   
     
def valid_fnd_move(src_card, dest_card):
    """
    This function is used to decide whether a movement from a tableau 
    or a cell to a foundation is valid or not. 
    The function will raise a RuntimeError exception if the move is not valid.
    """
    try:
       #if destination card is empty, source card should be ace
       if not dest_card and src_card.rank() !=1:  
           raise RuntimeError('Error: invalid move, fundation can be empty \
only when to move an ace')
       #if destination card is empty, source card should be ace
       elif src_card.rank()==1 and not dest_card: 
           return True
       elif not src_card: #if source card is empty
           raise RuntimeError('Error: Source Card is invalid')
           return False
       elif dest_card.rank()+1==src_card.rank() and \
src_card.suit()==dest_card.suit(): #check valid move
           return True
       else:
           raise RuntimeError('Invalid move: Source card is not an Ace')
           return False
    except RuntimeError as error_message:
       print("{:s}\nTry again.".format(str(error_message)))
        
def valid_tab_move(src_card, dest_card):
    """
    This function is used to decide whether a movement from a cell, foundation, 
    or another tableau to a tableau is valid or not
    The function will raise a RuntimeError exception if the move is not valid.
    """    
    try:
       if not src_card: #empty source card
           raise RuntimeError('Error: Source Card is invalid')
           return False
     #empty destination column is always valid to move to
       elif not dest_card:
           return True
       elif src_card.rank()-1==dest_card.rank() and \
src_card.suit()==dest_card.suit(): #check valid move
           return True
       else:
           raise RuntimeError('Error: Invalid move')
           return False
    except RuntimeError as error_message:
       print("{:s}\nTry again.".format(str(error_message)))
        
def tableau_to_cell(tab, cell):
    """
    This function will implement a movement of a card from a tableau to a cell. 
    If there is an invalid move, it will raise a RuntimeError exception. 
    When a user enters tc x y, this function will be used.
    """    
    flag=False
    if cell and tab: #check if valid when cell is not empty
       flag=valid_tab_move(tab[-1],cell[-1])
    if not cell: #cell is empty
       flag=valid_tab_move(tab[-1],cell)
    if flag==True:
       cell.append(tab[-1]) #add to cell
       tab.pop() #delete the last card of some column
                        
def tableau_to_foundation(tab, fnd):
    """
    This function will implement a movement of a card 
    from a tableau to a foundation. 
    If there is an invalid move, it will raise a RuntimeError exception. 
    When a user enters tf x y, this function will be used.
    """    
    flag=False
    if not tab: #column to move card from should not be empty
       raise RuntimeError('Invalid move: Source card is not an Ace')
    if fnd and tab: #check if valid when foundation is not empty
       flag=valid_fnd_move(tab[-1],fnd[-1])
    if not fnd: #fundation is empty
       flag=valid_fnd_move(tab[-1],fnd)
    if flag==True:
       fnd.append(tab[-1]) #add to foundation
       tab.pop() #delete the last card of some column           
            
def tableau_to_tableau(tab1, tab2):
    """
    This function will implement a movement of a card from one tableau column 
    to another tableau column. 
    If there is an invalid move, it will raise a RuntimeError exception. 
    When a user enters tt x y, this function will be used.
    """    
    src_card = tab1[-1]
    dest_card = tab2[-1]
    #check whether the move in valid
    try:
        valid_tab_move(src_card, dest_card)
        #add to tab2 and delete the card in tab1
        tab2.expend(tab1[-1])
        tab1.pop()        
    except:#invalid move
        pass

def cell_to_foundation(cell, fnd):
    """
    This function will implement a movement of a card from a cell to 
    a foundation. If there is an invalid move, it will raise a RuntimeError 
    exception. When a user enters cf x y, this function will be used.
    """    
    if fnd: #foundation not empty
       flag=valid_fnd_move(cell[-1],fnd[-1])
    if not fnd: #fundation is empty
       flag=valid_fnd_move(cell[-1],fnd)
    if flag==True:
       fnd.append(cell[-1]) #add to foundation
       cell.pop() #delete the last card of some column

def cell_to_tableau(cell, tab):
    """
    This function will implement a movement of a card from a cell to 
    a tableau column. If there is an invalid move, it will raise a RuntimeError 
    exception. When a user enters ct x y, this function will be used.
    """    
    if tab: #tab is not empty
       flag=valid_tab_move(cell[-1],tab[-1])
    if not tab: #tab column is empty
       flag=valid_tab_move(cell[-1],tab)
    if flag==True:
       tab.append(cell[-1]) #add to tab
       cell.pop() #delete the last card of cell
                           
def is_winner(foundations):
    """
    This function will be used to decide if a game was won. 
    A game has been won if all the foundation piles have 13 cards 
    and the top card on each of the pile is a King. This function 
    returns either True or False.
    """    
    flag=False
    for fnd in foundations:
       if len(fnd) !=13 or fnd[-1].rank() !=13:
           flag=True #not win
    if flag==True: #not win
       return False
    else:
       print (BANNER) #win
       return True

def setup_game():
    """
    The game setup function. It has 4 cells, 4 foundations, and 8 tableaus. All
    of these are currently empty. This function populates the tableaus from a
    standard card deck. 

    Tableaus: All cards are dealt out from left to right (meaning from tableau
    1 to 8). Thus we will end up with 7 cards in tableaus 1 through 4, and 6
    cards in tableaus 5 through 8 (52/8 = 6 with remainder 4).

    This function will return a tuple: (cells, foundations, tableaus)
    """
    
    #You must use this deck for the entire game.
    #We are using our cards.py file, so use the Deck class from it.
    stock = cards.Deck()
    stock.shuffle()
    #The game piles are here, you must use these.
    cells = [[], [], [], []]                    #list of 4 lists
    foundations = [[], [], [], []]              #list of 4 lists
    tableaus = [[], [], [], [], [], [], [], []] #list of 8 lists
    
    """ YOUR SETUP CODE GOES HERE """
    cards_in_tableaus = 7
    for j in range(cards_in_tableaus):
        if len(stock) < 8:
            for i in range(len(stock)):
                card = stock.deal()
                try:
                    tableaus[i].append(card)
                except ValueError:
                    continue
        else:
            for i in range(8):
                card = stock.deal()
                try:
                    tableaus[i].append(card)
                except ValueError:
                    continue
    
    return cells, foundations, tableaus

def display_game(cells, foundations, tableaus):
    """
    display_game takes four parameters, 
    which should be the lists representing the cells,foundations, and tableaus. 
    The cells and foundations should be displayed above the tableaus. 
    A non-empty cell should be displayed as the card within it, whereas 
    an empty cell should be displayed as [ ]. A non-empty foundation 
    will be displayed as the top card in the pile, while an empty foundation 
    will also be displayed as [ ]. The tableau is displayed below the cells 
    and foundations, and each column of the tableau will be displayed 
    downwards as shown in the sample below. An empty column will be displayed 
    by whitespace. 
    """
    #Labels for cells and foundations
    print("    =======Cells========  ====Foundations=====")
    print("     --1----2----3----4--  --1----2----3----4--")
    print("    ", end="")
    # to print a card using formatting, convert it to string:
    # print("{}".format(str(card)))
    for cell in cells:
        #print empty []
        if not cell:
            print(" [  ]",end="")
        else:#add new card
            print ("[" + "{:1s}".format(str(cell[-1]))+"]"+" ",end="")
    for found in foundations:
        if not found:#print empty []
           print(" ","[  ]",end="")
        else:#add new card
           print ("[" + "{:1s}".format(str(found[-1]))+"]"+" ",end="")
    print()
    #Labels for tableaus
    print("    =================Tableaus=================")
    print("    ---1----2----3----4----5----6----7----8---")
    #find the lagest value of cards in tableaus
    max_num = 0
    for i in tableaus:
        num_card = len(i)
        if num_card > max_num:
            max_num = num_card
    for x in range(max_num):
        column = 8
        for y in range(column):
            try:
                cards = tableaus[y][x]
                if y == 0:#print the first column 
                    print("{:>9s}".format(str(cards)),end="")
                if y > 0 and y < 7:#print the folowing columns
                    print("{:>5s}".format(str(cards)),end="")
                if y != 0 and y >= 7:#print the last column
                    print("{:>5s}".format(str(cards)))                
            except IndexError:
                print('    ',end='')
                
#HERE IS THE MAIN BODY OF OUR CODE
print(RULES)
cells, fnds, tabs = setup_game()
display_game(cells, fnds, tabs)
print(MENU)
command = input("prompt :> ").strip().lower()
while command != 'q':
    try:
        #if the command is not valid
        if not command:
           raise RuntimeError('Error: An invalid command')
        if len(command.split()) != 3:
            raise RuntimeError('Error: An invalid command')
        #print the rules and menu and shuffle the cards
        elif command.strip().lower() =='r':
            cells, fnds, tabs = setup_game()
            print(RULES)
            print(MENU)
        #print the menu of commands
        elif command.strip().lower() =='h':
            print(MENU)       
        else:
            #set the coordinate
            x = int(command.split()[1])
            y = int(command.split()[2])
            #excute the commands
            if command.split()[0].lower()=="tf":
                if x in range(0,9) and y in range(0,5):
                    tableau_to_foundation(tabs[x-1], fnds[y-1])
                else:
                    raise RuntimeError('x should be in range(0,9) \
and y should be in range(0,5)')
            elif command.split()[0].lower()=="tt":
                if x in range(0,9) and y in range(0,9):
                    tableau_to_tableau(tabs[x-1], tabs[y-1])
                else:
                    raise RuntimeError('x should be in range(0,9) \
and y should be in range(0,9)')
            elif command.split()[0].lower()=="tc":
                if x in range(0,9) and y in range(0,5):
                    tableau_to_cell(tabs[x-1], cells[y-1])
                else:
                    raise RuntimeError('x should be in range(0,9) \
and y should be in range(0,5)')
            elif command.split()[0].lower()=="cf":
                if x in range(0,5) and y in range(0,5):
                    cell_to_foundation(cells[x-1], fnds[y-1])
                else:
                    raise RuntimeError('x should be in range(0,5) \
and y should be in range(0,5)')
            elif command.split()[0].lower()=="ct":
                if x in range(0,5) and y in range(0,5):
                        cell_to_tableau(cells[x-1], tabs[y-1])
                else:
                    raise RuntimeError('x should be in range(0,5) \
and y should be in range(0,5)')
          
       #check win or not after each command
        foundations = setup_game()
        flag= is_winner(foundations)

       #quit game if win
        if flag==True:
           break
        
    #Any RuntimeError you raise lands here
    except RuntimeError as error_message:
        print("{:s}\nTry again.".format(str(error_message)))
    
    display_game(cells, fnds, tabs)                
    command = input("prompt :> ").strip().lower()


