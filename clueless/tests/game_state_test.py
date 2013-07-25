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
        player.game_cards = [
            game_state.GameCard(
                item=game_state.WRENCH,
                item_type=game_state.WEAPON
            ),
            game_state.GameCard(
                item=game_state.PEACOCK,
                item_type=game_state.SUSPECT
            )
        ]
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


class WhenTestingGameState(unittest.TestCase):

    def setUp(self):
        self.game_cards1 = [game_state.GameCard(
            item=game_state.WRENCH, item_type=game_state.WEAPON)]
        self.game_cards2 = [game_state.GameCard(
            item=game_state.REVOLVER, item_type=game_state.WEAPON)]
        self.players = [
            game_state.Player(
                username="testuser1",
                suspect=game_state.PLUM,
                game_cards=self.game_cards1),
            game_state.Player(
                username="testuser2",
                suspect=game_state.PEACOCK,
                game_cards=self.game_cards2)
        ]
        self.game_state = game_state.GameState(players=self.players)

    def test_format(self):
        game_state_dict = self.game_state.format()
        for player in self.game_state.players:
            self.assertTrue(player.format() in game_state_dict["players"])
        self.assertEqual(
            self.game_state.player_messages,
            game_state_dict["player_messages"]
        )
        for player in self.game_state.turn_list:
            self.assertTrue(player.format() in game_state_dict["turn_list"])
        self.assertEqual(
            self.game_state.current_player.format(),
            game_state_dict["current_player"]
        )
        self.assertEqual(
            self.game_state.turn_status,
            game_state_dict["turn_status"]
        )
        for game_card in self.game_state.case_file:
            self.assertTrue(
                game_card.format() in game_state_dict["case_file"]
            )
        for space in self.game_state.game_board:
            self.assertTrue(space.format() in game_state_dict["game_board"])


class WhenTestingGameStateBuilder(unittest.TestCase):
    def setUp(self):
        self.players = [
            game_state.Player(
                username="testuser1",
                suspect=game_state.PLUM
            ),
            game_state.Player(
                username="testuser2",
                suspect=game_state.PEACOCK
            )
        ]

    def test_create_game_state_from_dict(self):
        self.maxDiff = None
        self.game_state = game_state.GameState(self.players)
        game_state_dict = self.game_state.format()
        builder = game_state.GameStateBuilder()
        game_state_built = builder.build_gamestate_from_dict(game_state_dict)
        self.assertEqual(game_state_dict, game_state_built.format())
