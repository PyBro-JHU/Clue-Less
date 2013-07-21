"""
The game_state entities module contains the classes that represent
game entities for suspects, weapons, rooms, hallways, game cards,
and the game board
"""

import random


#constants for suspect names
SUSPECT = 'Suspect'

MUSTARD = 'Colonel Mustard'
SCARLET = 'Miss Scarlet'
PLUM = 'Professor Plum'
GREEN = 'Mr. Green'
WHITE = 'Mrs. White'
PEACOCK = 'Mrs. Peacock'

SUSPECTS = [
    MUSTARD,
    SCARLET,
    PLUM,
    GREEN,
    WHITE,
    PEACOCK
]

#constants for weapon names
WEAPON = 'Weapon'

ROPE = 'Rope'
LEAD_PIPE = 'Lead Pipe'
KNIFE = 'Knife'
WRENCH = 'Wrench'
CANDLESTICK = 'Candlestick'
REVOLVER = 'Revolver'

WEAPONS = [
    ROPE,
    LEAD_PIPE,
    KNIFE,
    WRENCH,
    CANDLESTICK,
    REVOLVER
]

#constants for rooms
ROOM = 'Room'
KITCHEN = 'Kitchen'
BALLROOM = 'Ballroom'
CONSERVATORY = 'Conservatory'
BILLIARD_ROOM = 'Billiard Room'
LIBRARY = 'Library'
STUDY = 'Study'
HALL = 'Hall'
LOUNGE = 'Lounge'
DINING_ROOM = 'Dining Room'

ROOMS = [
    KITCHEN,
    BALLROOM,
    CONSERVATORY,
    BILLIARD_ROOM,
    LIBRARY,
    STUDY,
    HALL,
    LOUNGE,
    DINING_ROOM
]

#constants for hallways
STUDY_LIBRARY = 'study-library hallway'
STUDY_HALL = 'study-hall ahllway'
HALL_BILLIARD = 'hall-billiard hallway'
HALL_LOUNGE = 'hall-lounge hallway'
LOUNGE_DINING = 'lounge-dining hallway'
LIBRARY_CONSERVATORY = 'library-conservatory hallway'
LIBRARY_BILLIARD = 'library-billiard hallway'
BILLIARD_BALLROOM = 'billiard-ballroom hallway'
BILLIARD_DINING = 'billiard-dining hallway'
DINING_KITCHEN = 'dining-kitchen hallway'
CONSERVATORY_BALLROOM = 'conservatory-ballroom hallway'
BALLROOM_KITCHEN = "ballroom-kitchen hallway"

HALLWAY = [
    STUDY_LIBRARY,
    STUDY_HALL,
    HALL_BILLIARD,
    HALL_LOUNGE,
    LOUNGE_DINING,
    LIBRARY_CONSERVATORY,
    LIBRARY_BILLIARD,
    BILLIARD_BALLROOM,
    BILLIARD_DINING,
    DINING_KITCHEN,
    CONSERVATORY_BALLROOM,
    BALLROOM_KITCHEN
]


class Player(object):
    """
    Player is an external user fo the system that will be playing the game
    """
    def __init__(self, username):
        self.username = username
        self.suspect = None
        self.game_cards = list()


class GameSpace(object):
    """
    GameSpace is an abstract super class used to define
    spaces on the game board
    """
    def __init__(self, name, connected_spaces):
        self.name = name
        self.connected_spaces = connected_spaces
        self.suspects = list()

    def is_available(self):
        raise NotImplementedError


class Room(GameSpace):
    """
    Room represents a room on the game board.
    It may contain suspects and weapons
    """
    def __init__(self, name, connected_spaces):
        super(Room, self).__init__(name, connected_spaces)
        self.suspects = None
        self.weapons = None

    def is_available(self):
        """
        A Room can hold more than one suspect at a time
        so it will always be available
        """
        return True


class Hallway(GameSpace):
    """
    Hallways represents the hallways between rooms on the GameBoard
    """
    def __init__(self, name, connected_spaces):
        super(Hallway, self).__init__(name, connected_spaces)
        self.suspect = None

    def is_available(self):
        """
        Only one suspect can be in a hallway at a time, so return
        True if empty or False if occupied
        """
        return not self.suspect


class HomeSquare(GameSpace):
    """
    HomeSquare represent the starting square for each suspect on the
    game board.  Starting squares may only have one occupant at a time
    and can not be moved to during a turn
    """
    def __init__(self, name, connected_spaces):
        super(HomeSquare, self).__init__(name, connected_spaces)
        self.suspect = None

    def is_available(self):
        """
        returns false because HomeSquares can not be moved to
        during regular game play
        """
        return False


class GameBoard(object):
    """
    The GameBoard creates a collections of HomeSquares, Rooms, and Hallways,
    and defines their relation to one another on the game board
    """
    def __init__(self):

      self.spaces = {
          KITCHEN: Room(
              name=KITCHEN,
              connected_spaces=[
                  DINING_KITCHEN,
                  BALLROOM_KITCHEN,
                  STUDY
              ]
          ),
          BALLROOM: Room(
              name=BALLROOM,
              connected_spaces=[
                  BALLROOM_KITCHEN,
                  CONSERVATORY_BALLROOM,
                  BILLIARD_BALLROOM
              ]
          ),
          CONSERVATORY: Room(
              name=CONSERVATORY,
              connected_spaces=[
                  CONSERVATORY_BALLROOM,
                  LIBRARY_CONSERVATORY,
                  LOUNGE
              ]
          ),
          BILLIARD_ROOM: Room(
              name=BILLIARD_ROOM,
              connected_spaces=[
                  HALL_BILLIARD,
                  LIBRARY_BILLIARD,
                  BILLIARD_BALLROOM,
                  BILLIARD_DINING
              ]
          ),
          LIBRARY:Room(
              name=LIBRARY,
              connected_spaces=[
                  STUDY_LIBRARY,
                  LIBRARY_CONSERVATORY,
                  LIBRARY_BILLIARD
              ]
          ),
          STUDY: Room(
              name=STUDY,
              connected_spaces=[
                  KITCHEN,
                  STUDY_LIBRARY,
                  STUDY_HALL
              ]
          ),
          HALL: Room(
              name=HALL,
              connected_spaces=[
                  STUDY_HALL,
                  HALL_BILLIARD,
                  HALL_LOUNGE
              ]
          ),
          LOUNGE: Room(
              name=LOUNGE,
              connected_spaces=[
                  CONSERVATORY,
                  HALL_LOUNGE,
                  LOUNGE_DINING
              ]
          ),
          DINING_ROOM: Room(
              name=DINING_ROOM,
              connected_spaces=[
                  LOUNGE_DINING,
                  BILLIARD_DINING,
                  DINING_KITCHEN
              ]
          ),
          STUDY_LIBRARY: Hallway(
              name=STUDY_LIBRARY,
              connected_spaces=[
                  STUDY,
                  LIBRARY
              ]
          ),
          STUDY_HALL: Hallway(
              name=STUDY_HALL,
              connected_spaces=[
                  STUDY,
                  HALL
              ]
          ),
          HALL_BILLIARD: Hallway(
              name=HALL_BILLIARD,
              connected_spaces=[
                  HALL,
                  BILLIARD_ROOM
              ]
          ),
          HALL_LOUNGE: Hallway(
              name=HALL_LOUNGE,
              connected_spaces=[
                  HALL,
                  LOUNGE
              ]
          ),
          LOUNGE_DINING: Hallway(
              name=LOUNGE_DINING,
              connected_spaces=[
                  LOUNGE,
                  DINING_ROOM
              ]
          ),
          LIBRARY_CONSERVATORY: Hallway(
              name=LIBRARY_CONSERVATORY,
              connected_spaces=[
                  LIBRARY,
                  CONSERVATORY
              ]),
          LIBRARY_BILLIARD: Hallway(
              name=LIBRARY_BILLIARD,
              connected_spaces=[
                  LIBRARY,
                  BILLIARD_ROOM
              ]
          ),
          BILLIARD_BALLROOM:  Hallway(
              name=BILLIARD_BALLROOM,
              connected_spaces=[
                  BILLIARD_ROOM,
                  BALLROOM
              ]
          ),
          BILLIARD_DINING: Hallway(
              name=BILLIARD_DINING,
              connected_spaces=[
                  BILLIARD_ROOM,
                  DINING_ROOM
              ]
          ),
          DINING_KITCHEN: Hallway(
              name=DINING_KITCHEN,
              connected_spaces=[
                  DINING_ROOM,
                  KITCHEN
              ]
          ),
          CONSERVATORY_BALLROOM: Hallway(
              name=CONSERVATORY_BALLROOM,
              connected_spaces=[
                  CONSERVATORY,
                  BALLROOM_KITCHEN
              ]
          ),
          BALLROOM_KITCHEN:  Hallway(
              name=BALLROOM_KITCHEN,
              connected_spaces=[
                  BALLROOM,
                  KITCHEN
              ]
          ),
          MUSTARD: HomeSquare(
              name=MUSTARD,
              connected_spaces=[
                  LOUNGE_DINING
              ]
          ),
          SCARLET: HomeSquare(
              name=SCARLET,
              connected_spaces=[
                  HALL_LOUNGE
              ]
          ),
          PLUM: HomeSquare(
              name=PLUM,
              connected_spaces=[
                  STUDY_LIBRARY
              ]
          ),
          GREEN: HomeSquare(
              name=GREEN,
              connected_spaces=[
                  CONSERVATORY_BALLROOM
              ]
          ),
          WHITE: HomeSquare(
              name=WHITE,
              connected_spaces=[
                  BALLROOM_KITCHEN
              ]
          ),
          PEACOCK: HomeSquare(
              name=PEACOCK,
              connected_spaces=[
                  LIBRARY_CONSERVATORY
              ]
          )
      }


class GameCard(object):
    """
    represents a single Clue-less game card
    """
    def __init__(self, item, item_type):
        self.item  = item
        self.type = item_type










