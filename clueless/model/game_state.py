"""
The game_state entities module contains the classes that represent
game entities for suspects, weapons, rooms, hallways, game cards,
and the game board
"""

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

HALLWAYS = [
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

#constants for turn state
AWAITING_MOVE = "Waiting for player to move"
AWAITING_SUGGESTION = "Waiting for player to make suggestion"
AWAITING_SUGGESTION_RESPONSE = "Waiting for response to player suggestion"


class GameCard(object):
    """
    represents a single Clue-less game card
    """
    def __init__(self, item, item_type):
        self.item = item
        self.type = item_type

    def format(self):
        """
        format the object as a dictionary.
        """
        return {
            "item": self.item,
            "type": self.type
        }


class Player(object):
    """
    Player is an external user fo the system that will be playing the game
    """
    def __init__(self, username, suspect=None,
                 game_cards=None, cards_seen=None):
        self.username = username
        if suspect:
            self.suspect = suspect
        else:
            self.suspect = None
        if game_cards:
            self.game_cards = game_cards
        else:
            self.game_cards = list()
        if cards_seen:
            self.cards_seen = cards_seen
        else:
            self.cards_seen = list()

    def format(self):
        """
        format the object as a dictionary.
        """
        return {
            "username": self.username,
            "suspect": self.suspect,
            "game_cards": [
                game_card.format() for game_card in self.game_cards
            ],
            "cards_seen": [
                game_card.format() for game_card in self.cards_seen
            ]
        }


class Suggestion(object):
    def __init__(self, suspect, weapon, room):
        self.suspect = suspect
        self.weapon = weapon
        self.room = room

    def format(self):
        return {
            "suspect": self.suspect,
            "weapon": self.weapon,
            "room": self.room
        }


class GameSpace(object):
    """
    GameSpace is an abstract super class used to define
    spaces on the game board
    """
    def __init__(self, name, connected_spaces, suspects=None):
        self.name = name
        self.connected_spaces = connected_spaces
        if suspects:
            self.suspects = suspects
        else:
            self.suspects = list()

    def is_available(self):
        raise NotImplementedError

    def format(self):
        """
        format the object as a dictionary.
        """
        return {
            "name": self.name,
            "connected_spaces":  self.connected_spaces,
            "suspects": self.suspects
        }


class Room(GameSpace):
    """
    Room represents a room on the game board.
    It may contain suspects and weapons
    """
    def __init__(self, name, connected_spaces, suspects=None, weapons=None):
        super(Room, self).__init__(name, connected_spaces, suspects)

        if weapons:
            self.weapons = weapons
        else:
            self.weapons = None

    def is_available(self):
        #A Room can hold more than one suspect at a time
        #so it will always be available
        return True

    def format(self):
        """
        format the object as a dictionary.  This method overrides the
        superclass format method in order to add the weapons attribute
        """
        return {
            "name": self.name,
            "connected_spaces": self.connected_spaces,
            "suspects": self.suspects,
            "weapons": self.weapons
        }


class Hallway(GameSpace):
    """
    Hallways represents the hallways between rooms on the GameBoard
    """
    def __init__(self, name, connected_spaces, suspects=None):
        super(Hallway, self).__init__(name, connected_spaces, suspects)

    def is_available(self):
        #Only one suspect can be in a hallway at a time, so return
        #True if empty or False if occupied
        return not (self.suspects)


class HomeSquare(GameSpace):
    """
    HomeSquare represent the starting square for each suspect on the
    game board.  Starting squares may only have one occupant at a time
    and can not be moved to during a turn
    """
    def __init__(self, name, connected_spaces, suspects=None):
        super(HomeSquare, self).__init__(name, connected_spaces, suspects)

    def is_available(self):
        #returns false because players can not move to
        #HomeSquares during regular play
        return False


class GameState(object):
    """
    GameState  creates all properties necessary to
    observe the state fo the Game in play
    """
    def __init__(self, players, player_messages=None, turn_list=None,
                 current_player=None, turn_status=None,
                 current_suggestion=None, suggestion_response_player=None,
                 case_file=None, game_board=None):

        self.players = players
        if player_messages:
            self.player_messages = player_messages
        else:
            self.player_messages = list()
        if turn_list:
            self.turn_list = turn_list
        else:
            self.turn_list = list(players)
        if current_player:
            self.current_player = current_player
        else:
            self.current_player = self.turn_list[0]
        if turn_status:
            self.turn_status = turn_status
        else:
            self.turn_status = AWAITING_MOVE

        self.current_suggestion = current_suggestion

        self.suggestion_response_player = suggestion_response_player

        #holds the winning cards
        if case_file:
            self.case_file = case_file
        else:
            self.case_file = list()

        #The game_board is a collections of HomeSquares, Rooms, and Hallways,
        #and defines their relation to one another on the game board
        if game_board:
            self.game_board = game_board
        else:
            self.game_board = {
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
                LIBRARY: Room(
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
                    ]
                ),
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
                    ],
                    suspects=[MUSTARD]
                ),
                SCARLET: HomeSquare(
                    name=SCARLET,
                    connected_spaces=[
                        HALL_LOUNGE
                    ],
                    suspects=[SCARLET]
                ),
                PLUM: HomeSquare(
                    name=PLUM,
                    connected_spaces=[
                        STUDY_LIBRARY
                    ],
                    suspects=[PLUM]
                ),
                GREEN: HomeSquare(
                    name=GREEN,
                    connected_spaces=[
                        CONSERVATORY_BALLROOM
                    ],
                    suspects=[GREEN]
                ),
                WHITE: HomeSquare(
                    name=WHITE,
                    connected_spaces=[
                        BALLROOM_KITCHEN
                    ],
                    suspects=[WHITE]
                ),
                PEACOCK: HomeSquare(
                    name=PEACOCK,
                    connected_spaces=[
                        LIBRARY_CONSERVATORY
                    ],
                    suspects=[PEACOCK]
                )
            }

    def format(self):
        """
        format the object as a dictionary.
        """
        return {
            "players": [
                player.format() for player in self.players
            ],
            "player_messages": self.player_messages,
            "turn_list": [
                player.format() for player in self.turn_list
            ],
            "current_player": self.current_player.format(),
            "turn_status": self.turn_status,
            "current_suggestion":
            self.current_suggestion.format()
            if self.current_suggestion else None,
            "suggestion_response_player":
            self.suggestion_response_player.format()
            if self.suggestion_response_player else None,
            "case_file": [card.format() for card in self.case_file],
            "game_board": {
                key: (self.game_board[key]).format()
                for key in self.game_board
            }
        }


class GameStateBuilder(object):
    def build_gamestate_from_dict(self, game_state_dict):

        #copy dictionary
        game_state = game_state_dict.copy()

        #build the list of Player objects
        game_state["players"] = self._build_players(game_state["players"])

        #reference the Player objects that are in the turn list
        game_state["turn_list"] = [
            player for player in game_state["players"]
            if player.username in [
                turn_list_player["username"]
                for turn_list_player in game_state["turn_list"]
            ]
        ]

        #reference the Player object for the current turn
        if game_state["current_player"]:
            game_state["current_player"] = [
                player for player in game_state["players"]
                if player.username == game_state["current_player"]["username"]
            ][0]

        if game_state["current_suggestion"]:
            game_state["current_suggestion"] = Suggestion(
                **game_state["current_suggestion"]
            )
        if game_state["suggestion_response_player"]:
            game_state["suggestion_response_player"] = [
                player for player in game_state["players"]
                if player.username ==
                game_state["suggestion_response_player"]["username"]
            ][0]

        #build the list of winning GameCard objects
        game_state["case_file"] = self._build_game_cards(
            game_state["case_file"])

        game_board = dict()
        #assign the lists of newly created gamespace objects to the game_board
        for key in game_state["game_board"]:
            if key in ROOMS:
                game_board[key] = Room(**game_state["game_board"][key])
            if key in HALLWAYS:
                game_board[key] = Hallway(**game_state["game_board"][key])
            if key in SUSPECTS:
                game_board[key] = HomeSquare(**game_state["game_board"][key])

        game_state["game_board"] = game_board

        #return a new GameState object built from the game state dictionary
        return GameState(**game_state)

    def _build_game_cards(self, game_cards):
        return [
            GameCard(**game_card_dict) for game_card_dict in game_cards
        ]

    def _build_players(self, players):
        for player_dict in players:
            player_dict["game_cards"] = self._build_game_cards(
                player_dict["game_cards"])
            player_dict["game_cards"] = self._build_game_cards(
                player_dict["cards_seen"])
        return [Player(**player_dict) for player_dict in players]
