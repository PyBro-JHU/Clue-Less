Clue-Less
=========

Clue-Less is a paython based implementation of the of the Clue boardgame.
The application is a team project for a graduate level Software Engineering Course at Johns Hopkins University.

**Project Details:**


This game is a simplified version of the popular board game, Clue®. The main simplification is in the navigation of the game board. In Clue-Less there are the same nine rooms, six weapons, and six people as in the board game. The rules are pretty much the same except for moving from room to room.

The rooms are laid out in a 3x3 grid with a hallway separating each pair of adjacent rooms.

Each hallway only holds one person. If someone is currently in a hallway, you may not move there.

When it is your turn, you don’t need to roll a die.


**Your options of moving are limited to the following:**

If you are in a room, you may do one of the following:

* Move through one of the doors to the hallway (if it is not blocked).

* Take a secret passage to a diagonally opposite room (if there is one) and make a suggestion.

If you were moved to the room by another player making a suggestion, you may, if you wish, stay in that room and make a suggestion. Otherwise you may move through a doorway or take a secret passage as described above.

If you are in a hallway, you must do the following:

* Move to one of the two rooms accessible from that hallway and make a suggestion.

			
If all of the exits are blocked (i.e., there are people in all of the hallways) and you are not in one of the corner rooms (with a secret passage), and you weren’t moved to the room by another player making a suggestion, you lose your turn (except for maybe making an accusation).

Your first move must be to the hallway that is adjacent to your home square.

Whenever a suggestion is made, the room must be the room the one making the suggestion is currently in. The suspect and weapon in the suggestion are moved to the room in the suggestion.

You may make an accusation at any time during your turn.

**Requirements for your computerized version of Clue-Less:**

Each player should access the game from a separate computer, with a graphical user interface.

The game rules are the same as in regular Clue except for the navigation (which is described above).

Each time the game state changes (a person is moved, a suggestion is made, a player disproves a suggestion, or a player is unable to disprove a suggestion) all players should be notified.

You should document the message interface to the Clue-Less server in your software requirements specification document.

Consider using a text based client for the minimal system, and a GUI version in the target. 

You can find the official Clue® game rules by downloading the following pdf file. Some of the rules may have changed in more recent editions of the game. We will be following the original rules:
[http://www.hasbro.com/common/instruct/clueins.pdf](http://www.hasbro.com/common/instruct/clueins.pdf)

The official Hasbro Clue game web site is:
[http://www.hasbro.com/games/en_US/clue/](http://www.hasbro.com/games/en_US/clue/)

