#!/usr/bin/env python

"""Scramble Solver

Usage:
  solver.py <cards>
  solver.py (-h | --help)
  solver.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from docopt import docopt
import yaml
import os

class Board(list):


    def __init__(self,*args,**kwargs):
        self.x = kwargs.get('x',3)
        self.y = kwargs.get('y',3)
        self.solution = []

    def is_valid_placement(self,deck):
        """
        Check the validity of the placement of the last card on the board
        """
        placement_location = len(self) - 1

        # Check top/bottom abutment if not a top row placement
        if placement_location >= self.x:
            (match1,pair1) = deck.get_image(self[placement_location-self.x],'bottom')
            (match2,pair2) = deck.get_image(self[placement_location],'top')
            if (match1 == match2) and (pair1 != pair2):
                # MATCH on UPPER edge, don't exit False yet
                pass
            else:
                return False

        # Check left/right abutment if not a left column placement
        if (placement_location) % self.y != 0:
            (match1,pair1) = deck.get_image(self[placement_location-1],'right')
            (match2,pair2) = deck.get_image(self[placement_location],'left')
            if (match1 == match2) and (pair1 != pair2):
                # MATCH on LEFT edge, don't exit False yet
                pass
            else:
                return False

        return True


    def place(self,deck):
        """ Recursive placer """
        if len(self) != deck.size():
            for idx in xrange(0,deck.size()):
                if idx not in [seq[0] for seq in self]:
                    for orient in [0,90,180,270]:
                        self.append( (idx,orient) ) 
                        if self.is_valid_placement(deck):
                            self.place(deck)
                        self.pop()
        else:
            if self.solution == []:
                #print "***COMPLETE*** {}".format( board )
                self.solution = self[:]
            else:
                r90 = self.rotate90()
                r180 = r90.rotate90()
                r270 = r180.rotate90()

                if ((r90 != board.solution) &
                   (r180 != board.solution) &
                   (r270 != board.solution)):
                    print "additional solution {}".format(self)

    def rotate90(self):
        retval = Board()
        for idx in [2,5,8,1,4,7,0,3,6]:
            retval.append( (self[idx][0], ((self[idx][1]+90)%360)) )
            #print "**{}".format(retval)
        return retval



class Deck(object):
    max_card_name_length = 10

    def __init__(self, file):
        self.max_str_len = 0
        with open(file) as fp:
            self.yml_data = yaml.load(fp)
            self.card_data = self.yml_data['cards']

        for card in self.card_data:
            for side in card:
                for idx in [0,1]:
                    card[side][idx] = card[side][idx][0:Deck.max_card_name_length]
                    if len(card[side][idx]) > self.max_str_len:
                        self.max_str_len = len(card[side][idx])

        #if self.max_str_len > 8:
        #    self.max_str_len = 8

        self.text_card_width = self.max_str_len * 3 + 4

    def size(self):
        return len(self.card_data) 

    def get_image(self, card_placement, side):
        """
        Return image description, given card number, orientation, and side
        """
        transform = dict()
        for orient in ['left','bottom','right','top']:
            transform[orient] = dict()

        transform['left'][0]     = 'left'
        transform['left'][90]    = 'top'
        transform['left'][180]   = 'right'
        transform['left'][270]   = 'bottom'
        transform['top'][0]      = 'top'
        transform['top'][90]     = 'right'
        transform['top'][180]    = 'bottom'
        transform['top'][270]    = 'left'
        transform['right'][0]    = 'right'
        transform['right'][90]   = 'bottom'
        transform['right'][180]  = 'left'
        transform['right'][270]  = 'top'
        transform['bottom'][0]   = 'bottom'
        transform['bottom'][90]  = 'left'
        transform['bottom'][180] = 'top'
        transform['bottom'][270] = 'right'
        (idx,orient) = card_placement
        image = (self.card_data[idx][transform[side][orient]])
        return (image[0], image[1])


if __name__ == "__main__":

    arguments = docopt(__doc__, version='solver.py 0.0.1')
    file = arguments['<cards>']

    deck = Deck(file)
    board = Board()
    board.place( deck )

    div_str = (("+{}".format("-"*deck.text_card_width))*3)+"+"
    spc_str = (("|{}".format(" "*deck.text_card_width))*3)+"|"
    lr_str = ((" {:"+str(deck.max_str_len)+"}")*2)+" {:>"+str(deck.max_str_len)+"} "


    if board.solution:
        for row in [0,1,2]:
            print div_str

            for idx in [0,1]:
                print("|{}|{}|{}|".format( 
                      (deck.get_image(board.solution[3*row+0],'top')[idx]).center(deck.text_card_width),
                      (deck.get_image(board.solution[3*row+1],'top')[idx]).center(deck.text_card_width), 
                      (deck.get_image(board.solution[3*row+2],'top')[idx]).center(deck.text_card_width)))

            print spc_str

            for idx in [0,1]:
                print("|{}|{}|{}|".format( 
                      lr_str.format(
                          deck.get_image(board.solution[3*row+0],'left')[idx],
                          " ",
                          deck.get_image(board.solution[3*row+0],'right')[idx]),
                      lr_str.format(
                          deck.get_image(board.solution[3*row+1],'left')[idx],
                          " ",
                          deck.get_image(board.solution[3*row+1],'right')[idx]),
                      lr_str.format(
                          deck.get_image(board.solution[3*row+2],'left')[idx],
                          " ",
                          deck.get_image(board.solution[3*row+2],'right')[idx]) ))


            print spc_str

            for idx in [0,1]:
                print("|{}|{}|{}|".format( 
                      (deck.get_image(board.solution[3*row+0],'bottom')[idx]).center(deck.text_card_width),
                      (deck.get_image(board.solution[3*row+1],'bottom')[idx]).center(deck.text_card_width), 
                      (deck.get_image(board.solution[3*row+2],'bottom')[idx]).center(deck.text_card_width)))

        print div_str
