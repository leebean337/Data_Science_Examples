#Stil to do: Create pretty 'You win' logo,
#Unicode fix
#code within specified length
#incorporate any feedback
#project description + reflection paper

import random

class Colors:
    """ Class used for color printing of cards and messages
    """
    red = '\033[31m'
    bold = '\033[1m'
    black = '\033[0m'
    blue = '\033[94m'
    green = '\033[32m'

class Card:

    rank_dict = {' A':1,' 2':2, ' 3':3, ' 4':4, ' 5':5, ' 6':6, ' 7':7,
    ' 8':8, ' 9':9, '10':10, ' J':11, ' Q':12, ' K':13}

    suit_dict = {'S':1, 'H':2, 'D':3, 'C':4}

    def __init__(self, rank, suit, hidden=0):
        self.suit = suit
        self.rank = rank
        self.points = self.rank_dict[rank]
        self.suitorder = self.suit_dict[suit]
        self.hidden = hidden #for now don't hide cards
        if self.suit in "SC":
            self.black = True
        else:
            self.black = False

    def __repr__(self):
        #return f'{self.rank} of {self.suit}'
        if self.hidden == 1:
            return f'  ***  '
        elif self.hidden == 0 and self.suit in "HD":
            return Colors.red + f'{self.rank} of {self.suit}' + Colors.black
        else:
            return f'{self.rank} of {self.suit}'

    def __str__(self):
        if self.hidden == 1:
            return f'  ***  '
        elif self.hidden == 0 and self.suit in "HD":
            return Colors.red + f'{self.rank} of {self.suit}' + Colors.black
        else:
            return f'{self.rank} of {self.suit}'

class Deck(Card):
    """ Generates and shuffles a list of 52 object 'Card'
    """

    def __init__(self):
        #generate 52 card stack
        self.stack = [Card(rank,suit,hidden=1) for suit in ["S","H","D","C"]
        for rank in [" 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10",
        " J", " Q", " K", " A"]]

        #shuffles 52 card deck
        random.shuffle(self.stack)

        #create a pile list, where each item is a list of the cards in that pile
        self.pile = ["",]*8
        self.pile[0] = [] #just a spaceholder so we can keep numbers in order
        self.pile[1] = [self.stack[0]]
        self.pile[2] = [x for x in self.stack[1:3]]
        self.pile[3] = [x for x in self.stack[3:6]]
        self.pile[4] = [x for x in self.stack[6:10]]
        self.pile[5] = [x for x in self.stack[10:15]]
        self.pile[6] = [x for x in self.stack[15:21]]
        self.pile[7] = [x for x in self.stack[21:28]]
        for i in range(1,8):
            self.pile[i][-1].hidden=0

        #create the waste pile, put next card in the stack in the waste pile
        self.waste = [self.stack[28]]
        self.waste[0].hidden=0 #unhide first card in the waste pile
        self.stack = self.stack[29:]

        #create the foundation list, containing 5 items, a list for each suit
        #firts one empty, then each list corresponds to suit rank dict
        self.foundation = ["",]*5

    def print_board(self):
        """ Function to print board
        """

        #Find maximum pile length to determine how far to print
        self.max_length = 0
        for i in range(1,8):
            if len(self.pile[i]) > self.max_length:
                self.max_length = len(self.pile[i])

        print("                                       Type 'Q' for Quit")
        print("_________________________________________________________")

        print(Colors.bold + "|   S   |   H   |   D   |   C   |       |   P   |   N   |" + Colors.black)

        #print row of last foundation cards and current available play card
        for i in range(1,5):
            if self.foundation[i] != "":
                print(f"|{self.foundation[i][-1]}",end="")
            else:
                print(f"|       ",end="")

        #print last card in the waste pile, if its empty, print empty
        if self.waste == [] and self.stack != []:
            print(f"|       |       |  ***  |")
        elif self.waste == [] and self.stack == []:
            print(f"|       |       |       |")
        elif self.waste != [] and self.stack != []:
            print(f"|       |{self.waste[-1]}|  ***  |")
        else:
            print(f"|       |{self.waste[-1]}|       |")

        print("---------------------------------------------------------")
        print(Colors.bold + "|   1   |   2   |   3   |   4   |   5   |   6   |   7   |" + Colors.black)

        for j in range(0,self.max_length): #represents the row to print
            for i in range(1,8): #represents the pile to print
                if len(self.pile[i]) >= j+1:
                    print(f"|{self.pile[i][j]}",end="")
                else:
                    print(f"|       ",end="")
            print("|")
        print("")
        return

    def player_move(self):
        """ Gets players desired start and end card location for each play
            and error checks the play
        """

        #game continues until user selects Q for Quit
        self.start = ""
        self.end = ""
        while self.start != "q" and self.end != "q":

            self.print_board()

            #check if user inputs valid positions
            valid = False
            while valid == False:
                self.start = input(Colors.blue + "Location of card to move (choose PN or 1234567): " + Colors.black).lower()
                if self.start in "nq": #chance to quit the game
                    break
                self.end = input(Colors.blue + "Location of where to move it to (1234567 or SHDC): " + Colors.black).upper()
                if self.end == "q": #another chance to quit the game
                    break
                if self.start not in "p1234567" or self.end not in "1234567SHDC":
                    print(Colors.green + "Not a valid response, please try again" + Colors.black)
                else:
                    valid = True

            if self.start == "q" or self.end == "q":
                break

            #Separate functions for each type of move:
            #Tableau to Tableau moves (1234567 to 1234567)
            if self.start in "1234567" and self.end in "1234567":
                self.move_in_tableau()
            #Waste to Tableau move (P to 1234567)
            if self.start in "p" and self.end in "1234567":
                self.move_waste_tableau()
            #Tableau to Foundation (1234567 to SHDC)
            if self.start in "1234567" and self.end in "SHDC":
                self.move_tableau_foundation()
            #Waste to Foundation (P to SHDC)
            if self.start in "p" and self.end in "SHDC":
                self.move_waste_foundation()
            #Next card play
            if self.start in "n":
                self.next_card()

            #offer to quit game if no hidden cards on the Tableau
            self.hidden_status = 0
            for i in range(1,8):
                for card in self.pile[i]:
                    self.hidden_status += card.hidden
            if self.hidden_status == 0:
                print(Colors.green + f"There are no more hidden cards so it looks like you won!")
                self.start = 'q'

            #print you win! if foundation is complete (13 items in each list)
            self.cards_in_foundation = 0
            for i in range(1,5):
                self.cards_in_foundation += len(self.foundation[i])
            if self.cards_in_foundation == 52:
                print(Colors.green + f"Congratulations, you win!!!!")
                self.start = 'q'

    def next_card(self):
        """ Method to play next card from the stack to the waste pile
        """

        #if the stack is empty, return the stack
        if self.stack == []:
            self.return_stack()

        else:
            #adds first card in stack as last card in pile
            self.waste.extend([self.stack[0]])
            self.waste[-1].hidden=0 #unhided that card
            self.stack = self.stack[1:] #removes that card from the stack

        #if waste stack is empty?

    def return_stack(self):
        """ Method to return waste pile to the stack once stack is empty
        """

        self.stack = self.waste
        for x in self.stack:
            x.hidden=1
        self.waste = []

        #if after adjustmnet, stack is still empty, return that message:
        if self.stack == []:
            print(Colors.green + f"You have no more cards in the stack" + Colors.black)

    def move_single_card_from_pile(self):
        #remove single card from origin pile
        self.pile[int(self.start)] = self.pile[int(self.start)][:-1]
        #flip over last card if it is hidden (and if list not empty)
        if self.pile[int(self.start)] != []:
            if self.pile[int(self.start)][-1].hidden == 1:
                self.pile[int(self.start)][-1].hidden = 0

    def move_waste_tableau(self):
        """ Method to move card from the waste pile to the tableau
        """
        # Kings to empty lists
        if self.pile[int(self.end)] == []:
            if self.waste[-1].points == 13:
                self.pile[int(self.end)] = [self.waste[-1]]
                self.waste = self.waste[:-1]

        else:
        # check if card is sequential
            if self.pile[int(self.end)][-1].points == 1 + self.waste[-1].points:
                    #check if cards are opposite suit
                if self.pile[int(self.end)][-1].black != self.waste[-1].black:

                    #move single card to new spot and remove card from waste pile
                    self.pile[int(self.end)].extend([self.waste[-1]])
                    self.waste = self.waste[:-1]

                else:
                    print(Colors.green + f"Invalid move, must be opposite colored card" + Colors.black)
            else:
                print(Colors.green + f"Invalid move, only place sequentially lower cards question pile"  + Colors.black)


    def move_in_tableau(self):
        """ Method to move card from one pile in the tableau to another
            However, current only moves one card, need to allow for multiple cards
        """

        # Kings to empty lists
        if self.pile[int(self.end)] == []:
            self.top_card_to_move=""
            for i in range(0,len(self.pile[int(self.start)])):
                if self.pile[int(self.start)][i].hidden == 0:
                    if self.pile[int(self.start)][i].points == 13:
                        self.pile_to_move = self.pile[int(self.start)][i:]
                        self.top_card_to_move = self.pile[int(self.start)][i]
                        self.temp_newpile = self.pile[int(self.start)][:i]
                        break
            if self.top_card_to_move=="":
                print(Colors.green + f"Error: You can only place a King on an empty pile" + Colors.black)
            else:
                #move cards to new spot and remove card from old spot
                self.pile[int(self.end)].extend(self.pile_to_move)
                #remove stack of cards from origin pile
                self.pile[int(self.start)] = self.temp_newpile
                #flip over last card if it is hidden (and if list not empty)
                if self.pile[int(self.start)] != []:
                    if self.pile[int(self.start)][-1].hidden == 1:
                        self.pile[int(self.start)][-1].hidden = 0

        else:
            # For stacks to other non-empty stacks
            self.target = self.pile[int(self.end)][-1].points
            self.top_card_to_move=""
            for i in range(0,len(self.pile[int(self.start)])):
                if self.pile[int(self.start)][i].hidden == 0:
                    if self.pile[int(self.start)][i].points == self.target - 1:
                        self.pile_to_move = self.pile[int(self.start)][i:]
                        self.top_card_to_move = self.pile[int(self.start)][i]
                        self.temp_newpile = self.pile[int(self.start)][:i]
                        break
            if self.top_card_to_move=="":
                print(Colors.green + f"Error: No available cards to place on new pile" + Colors.black)
            else:
                #check if cards are opposite suit
                if self.pile[int(self.end)][-1].black != self.top_card_to_move.black:

                    #move cards to new spot and remove card from old spot
                    self.pile[int(self.end)].extend(self.pile_to_move)

                    #remove stack of cards from origin pile
                    self.pile[int(self.start)] = self.temp_newpile

                    #flip over last card if it is hidden (and if list not empty)
                    if self.pile[int(self.start)] != []:
                        if self.pile[int(self.start)][-1].hidden == 1:
                            self.pile[int(self.start)][-1].hidden = 0

                else:
                    print(Colors.green + f"Invalid move, must be opposite colored card" + Colors.black)


    def move_tableau_foundation(self):
        """ Method to move a single card from tableau pile to Foundation
        """
        # check if suit is being put on the right Foundation
        self.suit_locate = self.suit_dict[self.end] #numerical location of list
        if self.suit_locate != self.pile[int(self.start)][-1].suitorder:
            print(Colors.green + f"Error: you must place the correct suit on each foundation" + Colors.black)
        else:

            # check if foundation stack is empty, accepts .value 1 only
            if self.foundation[self.suit_locate] == "":
                if self.pile[int(self.start)][-1].points == 1:
                    self.foundation[self.suit_locate] = [self.pile[int(self.start)][-1]]
                    self.move_single_card_from_pile()

                else:
                    print(Colors.green + f"Error: You can only place an Ace on an empty foundation" + Colors.black)

            #Depending on numbers of items in list, accept only the one with the next value
            else:
                self.num_items = len(self.foundation[self.suit_locate])
                if self.pile[int(self.start)][-1].points == 1+self.num_items:
                    self.foundation[self.suit_locate].extend([self.pile[int(self.start)][-1]])
                    self.move_single_card_from_pile()

                else:
                    print(Colors.green + f"Error: You can only place cards in sequential order" + Colors.black)


    def move_waste_foundation(self):
        """ Method to move a single card from the waste pile to Foundation
        """
        # check if suit is being put on the right Foundation
        self.suit_locate = self.suit_dict[self.end] #numerical location of list
        if self.suit_locate != self.waste[-1].suitorder:
            print(Colors.green + f"Error: you must place the correct suit on each foundation" + Colors.black)
        else:

            # check if foundation stack is empty, accepts .value 1 only
            if self.foundation[self.suit_locate] == "":
                if self.waste[-1].points == 1:
                    self.foundation[self.suit_locate] = [self.waste[-1]]
                    self.waste = self.waste[:-1]
                else:
                    print(Colors.green + f"Error: You can only place an Ace on an empty foundation" + Colors.black)

            #Depending on numbers of items in list, accept only the one with the next value
            else:
                self.num_items = len(self.foundation[self.suit_locate])
                if self.waste[-1].points == 1+self.num_items:
                    self.foundation[self.suit_locate].extend([self.waste[-1]])
                    self.waste = self.waste[:-1]
                else:
                    print(Colors.green + f"Error: You can only place cards in sequential order" + Colors.black)

game = Deck()
game.player_move()
