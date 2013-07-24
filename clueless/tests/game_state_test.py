import unittest
from clueless import game_state



class WhenTestingGameCard(unittest.TestCase):

    def test_format(self):
        game_card = game_state.GameCard(
            item=game_state.WRENCH, item_type=game_state.WEAPON)
        card__dict = game_card.format()
        self.assertEqual(game_card.item, card__dict["item"])
        self.assertEqual(game_card.type, card__dict["type"])

class WhenTestingPlayer(unittest.TestCase):

    def test_format(self):
        player = game_state.Player(username="testuser")
        player.suspect = game_state.PLUM
        player.game_cards = [game_state.GameCard(item=game_state.WRENCH, item_type=game_state.WEAPON), game_state.GameCard(item=game_state.PEACOCK, item_type=game_state.SUSPECT)]
        player_dict = player.format()
        self.assertEqual(player.username, player_dict["username"])
        self.assertEqual(player.suspect, player_dict["suspect"])
        for game_card in player.game_cards:
            self.assertTrue(game_card.format() in player_dict["game_cards"])


class WhenTestingGameSpace(unittest.TestCase):

    def test_format(self):
        game_space = game_state.GameSpace(
            name=game_state.PLUM,
            connected_spaces=[game_state.STUDY_LIBRARY],
            suspects=[game_state.PLUM]
        )
        space_dict = game_space.format()
        self.assertEqual(game_space.name, space_dict["name"])
        self.assertEqual(
            game_space.connected_spaces, space_dict["connected_spaces"])
        self.assertEqual(game_space.suspects, space_dict["suspects"])


class WhenTestingRoom(unittest.TestCase):

    def setUp(self):
        self.room = game_state.Room(
            name=game_state.STUDY,
            connected_spaces=[game_state.STUDY_LIBRARY, game_state.STUDY_HALL],
            suspects=[game_state.PLUM, game_state.PEACOCK],
            weapons=[game_state.WRENCH, game_state.REVOLVER]
        )

    def test_is_available_returns_true(self):
        self.assertTrue(self.room.is_available())

    def test_format(self):
        room_dict = self.room.format()
        self.assertEqual(self.room.name, room_dict["name"])
        self.assertEqual(
            self.room.connected_spaces, room_dict["connected_spaces"])
        self.assertEqual(self.room.weapons, room_dict["weapons"])
        self.assertEqual(self.room.suspects, room_dict["suspects"])


class WhenTestingHallway(unittest.TestCase):

    def setUp(self):
        self.hallway = game_state.Hallway(
            name=game_state.BALLROOM_KITCHEN,
            connected_spaces=[
                game_state.BALLROOM,
                game_state.KITCHEN
            ]
        )

    def test_is_available_returns_false_if_suspect_in_hallway(self):
        self.hallway.suspects = [game_state.PLUM]
        self.assertFalse(self.hallway.is_available())

    def test_is_available_returns_true_if_no_suspect_in_hallway(self):

        self.assertTrue(self.hallway.is_available())

    def test_format(self):
        hallway_dict = self.hallway.format()
        self.assertEqual(self.hallway.name, hallway_dict["name"])
        self.assertEqual(
            self.hallway.connected_spaces, hallway_dict["connected_spaces"])
        self.assertEqual(self.hallway.suspects, hallway_dict["suspects"])


class WhenTestingHomeSquare(unittest.TestCase):

    def setUp(self):
        self.home_square = game_state.HomeSquare(
            name=game_state.MUSTARD,
            connected_spaces=[
                game_state.LOUNGE_DINING
            ],
            suspects=[game_state.MUSTARD]
        )

    def test_is_available_always_returns_false(self):
        self.assertFalse(self.home_square.is_available())

    def test_format(self):
        home_square_dict = self.home_square.format()
        self.assertEqual(self.home_square.name, home_square_dict["name"])
        self.assertEqual(
            self.home_square.connected_spaces,
            home_square_dict["connected_spaces"]
        )
        self.assertEqual(
            self.home_square.suspects, home_square_dict["suspects"])
