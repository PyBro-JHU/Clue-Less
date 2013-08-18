
import os
import webbrowser

import kivy
kivy.require('1.1.3')

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Ellipse, Color

from clueless.client import errors
from clueless.client import game_play
from clueless.model import game_state
from clueless.client.hci import help

class DisableButton(Button):
    def __init__(self, **kwargs):
        self.disabled = False
        super(DisableButton, self).__init__(**kwargs)
    def on_touch_down(self, touch):
        if (not self.disabled):
            super(DisableButton, self).on_touch_down(touch)
    def on_touch_move(self, touch):
        if (not self.disabled):
            super(DisableButton, self).on_touch_move(touch)
    def on_touch_up(self, touch):
        if (not self.disabled):
            super(DisableButton, self).on_touch_up(touch)
    def on_press(self):
        if (not self.disabled):
            super(DisableButton, self).on_press()
    def on_release(self):
        if (not self.disabled):
            super(DisableButton, self).on_release()
    def trigger_action(self, duration=0.1):
        if (not self.disabled):
            super(DisableButton, self).trigger_action(duration)
            
class GameTile(DisableButton, Widget):
    pass

class StartScreen(Screen):
    username = ObjectProperty(None)
    suspect = ObjectProperty(None)
    
    def __init__(self, client, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.client = client
        
    def register_player(self):
        try:
            self.client.register_player(self.username.text)
            try:
                self.client.choose_suspect(self.username.text, self.suspect.text)
                self.manager.get_screen('game').start_game(self.username.text)
                self.manager.current = self.manager.next()
            except errors.GameClientException:
                p = ErrorPopup(message="Suspect unavailable. Please select a different Suspect.")
                p.open()
        except errors.GameClientException:
            p = ErrorPopup(message="Invalid Username. Please provide a valid Username.")
            p.open()

class GameScreen(Screen):
    gameboard = ObjectProperty(0)
    controls = ObjectProperty(0)
    
    def __init__(self, client, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.client = client
        self.state = None
        Clock.schedule_interval(self.update, 1 / 30.)
        
    def start_game(self, username):
        self.username = username
        try:
            self.state = self.client.start_new_game()
            self.game_id = self.state.game_id
        except errors.GameClientException:
            p = ErrorPopup(message="Unable to start a new game. Please try again.")
            p.open()

    def update(self, dt):
        if self.state != None:
            try:
                self.state = self.client.get_game_state(self.game_id)
            except errors.GameClientException:
                print "ERROR: Could not get the game state."
            self.gameboard.update(self.client, 
                                  self.state,
                                  self.username)
            self.controls.update(self.client, 
                                 self.state,
                                 self.username)

    def display_help(self):
        try:
            help.open()
        except:
            pass
                
    def quit_game(self):
        try:
            self.client.destroy_game(self.game_id)
            self.state=None
            self.manager.current = self.manager.previous()
        except errors.GameClientException:
            p = ErrorPopup(message="Unable to end game. Please try again.")
            p.open()

class Gameboard(FloatLayout):
    study = ObjectProperty(None)
    study_hall = ObjectProperty(None)
    hall = ObjectProperty(None)
    hall_lounge = ObjectProperty(None)
    lounge = ObjectProperty(None)
    study_library = ObjectProperty(None)
    study_billiard = ObjectProperty(None)
    hall_billiard = ObjectProperty(None)
    lounge_billiard = ObjectProperty(None)
    lounge_dining = ObjectProperty(None)
    library = ObjectProperty(None)
    library_billiard = ObjectProperty(None)
    billiard_room = ObjectProperty(None)
    billiard_dining = ObjectProperty(None)
    dining_room = ObjectProperty(None)
    library_conservatory = ObjectProperty(None)
    conservatory_billiard = ObjectProperty(None)
    billiard_ballroom = ObjectProperty(None)
    kitchen_billiard = ObjectProperty(None)
    dining_kitchen = ObjectProperty(None)
    conservatory = ObjectProperty(None)
    conservatory_ballroom = ObjectProperty(None)
    ballroom = ObjectProperty(None)
    ballroom_kitchen = ObjectProperty(None)
    kitchen = ObjectProperty(None)
    
    COLORS = {game_state.SCARLET: (1.,0,0),
              game_state.PEACOCK: (0,0,1.),
              game_state.PLUM: (1.,0,1.),
              game_state.GREEN: (0,1.,0),
              game_state.WHITE: (1.,1.,1.),
              game_state.MUSTARD: (1.,1.,0)}
    
    def __init__(self, **kwargs):
        super(Gameboard, self).__init__(**kwargs)
        self.state = None
        
    def disable_tiles(self):
        self.study.disabled=True; self.study.canvas.opacity=.5
        self.study_hall.disabled=True; self.study_hall.canvas.opacity=.5
        self.hall.disabled=True; self.hall.canvas.opacity=.5
        self.hall_lounge.disabled=True; self.hall_lounge.canvas.opacity=.5
        self.lounge.disabled=True; self.lounge.canvas.opacity=.5
        self.study_library.disabled=True; self.study_library.canvas.opacity=.5
        self.hall_billiard.disabled=True; self.hall_billiard.canvas.opacity=.5
        self.lounge_dining.disabled=True; self.lounge_dining.canvas.opacity=.5
        self.library.disabled=True; self.library.canvas.opacity=.5
        self.library_billiard.disabled=True; self.library_billiard.canvas.opacity=.5
        self.billiard_room.disabled=True; self.billiard_room.canvas.opacity=.5
        self.billiard_dining.disabled=True; self.billiard_dining.canvas.opacity=.5
        self.dining_room.disabled=True; self.dining_room.canvas.opacity=.5
        self.library_conservatory.disabled=True; self.library_conservatory.canvas.opacity=.5
        self.billiard_ballroom.disabled=True; self.billiard_ballroom.canvas.opacity=.5
        self.dining_kitchen.disabled=True; self.dining_kitchen.canvas.opacity=.5
        self.conservatory.disabled=True; self.conservatory.canvas.opacity=.5
        self.conservatory_ballroom.disabled=True; self.conservatory_ballroom.canvas.opacity=.5
        self.ballroom.disabled=True; self.ballroom.canvas.opacity=.5
        self.ballroom_kitchen.disabled=True; self.ballroom_kitchen.canvas.opacity=.5
        self.kitchen.disabled=True; self.kitchen.canvas.opacity=.5

    def enable_tiles(self):
        self.study.disabled=False; self.study.canvas.opacity=1
        self.study_hall.disabled=False; self.study_hall.canvas.opacity=1
        self.hall.disabled=False; self.hall.canvas.opacity=1
        self.hall_lounge.disabled=False; self.hall_lounge.canvas.opacity=1
        self.lounge.disabled=False; self.lounge.canvas.opacity=1
        self.study_library.disabled=False; self.study_library.canvas.opacity=1
        self.hall_billiard.disabled=False; self.hall_billiard.canvas.opacity=1
        self.lounge_dining.disabled=False; self.lounge_dining.canvas.opacity=1
        self.library.disabled=False; self.library.canvas.opacity=1
        self.library_billiard.disabled=False; self.library_billiard.canvas.opacity=1
        self.billiard_room.disabled=False; self.billiard_room.canvas.opacity=1
        self.billiard_dining.disabled=False; self.billiard_dining.canvas.opacity=1
        self.dining_room.disabled=False; self.dining_room.canvas.opacity=1
        self.library_conservatory.disabled=False; self.library_conservatory.canvas.opacity=1
        self.billiard_ballroom.disabled=False; self.billiard_ballroom.canvas.opacity=1
        self.dining_kitchen.disabled=False; self.dining_kitchen.canvas.opacity=1
        self.conservatory.disabled=False; self.conservatory.canvas.opacity=1
        self.conservatory_ballroom.disabled=False; self.conservatory_ballroom.canvas.opacity=1
        self.ballroom.disabled=False; self.ballroom.canvas.opacity=1
        self.ballroom_kitchen.disabled=False; self.ballroom_kitchen.canvas.opacity=1
        self.kitchen.disabled=False; self.kitchen.canvas.opacity=1

    def update(self, client, state, username):
        self.client = client
        self.state = state
        self.username = username
        
        TILES = {game_state.STUDY: self.study,
                 game_state.STUDY_HALL: self.study_hall,
                 game_state.HALL: self.hall,
                 game_state.HALL_LOUNGE: self.hall_lounge,
                 game_state.LOUNGE: self.lounge,
                 game_state.STUDY_LIBRARY: self.study_library,
                 game_state.HALL_BILLIARD: self.hall_billiard,
                 game_state.LOUNGE_DINING: self.lounge_dining,
                 game_state.LIBRARY: self.library,
                 game_state.LIBRARY_BILLIARD: self.library_billiard,
                 game_state.BILLIARD_ROOM: self.billiard_room,
                 game_state.BILLIARD_DINING: self.billiard_dining,
                 game_state.DINING_ROOM: self.dining_room,
                 game_state.LIBRARY_CONSERVATORY: self.library_conservatory,
                 game_state.BILLIARD_BALLROOM: self.billiard_ballroom,
                 game_state.DINING_KITCHEN: self.dining_kitchen,
                 game_state.CONSERVATORY: self.conservatory,
                 game_state.CONSERVATORY_BALLROOM: self.conservatory_ballroom,
                 game_state.BALLROOM: self.ballroom,
                 game_state.BALLROOM_KITCHEN: self.ballroom_kitchen,
                 game_state.KITCHEN: self.kitchen,
                 game_state.SCARLET: self.hall_lounge,
                 game_state.PEACOCK: self.library_conservatory,
                 game_state.PLUM: self.study_library,
                 game_state.GREEN: self.conservatory_ballroom,
                 game_state.WHITE: self.ballroom_kitchen,
                 game_state.MUSTARD: self.lounge_dining}

        self.hall_lounge.canvas.after.clear()
        self.library_conservatory.canvas.after.clear()
        self.study_library.canvas.after.clear()
        self.conservatory_ballroom.canvas.after.clear()
        self.ballroom_kitchen.canvas.after.clear()
        self.lounge_dining.canvas.after.clear()
        
        for name, room in self.state.game_board.iteritems():
            tile = TILES[room.name]
            if tile != self.hall_lounge and \
               tile != self.library_conservatory and \
               tile != self.study_library and \
               tile != self.conservatory_ballroom and \
               tile != self.ballroom_kitchen and \
               tile != self.lounge_dining:
                tile.canvas.after.clear()
            if name in game_state.SUSPECTS:
                if game_state.SCARLET in room.suspects:
                    y = self.hall_lounge.top-self.hall_lounge.height/4
                    x = self.hall_lounge.right-self.hall_lounge.width/2
                    with self.hall_lounge.canvas.after:
                        Color(*self.COLORS[game_state.SCARLET])
                        Ellipse(pos=(x-7.5, y-7.5), size=(15,15))
                if game_state.PEACOCK in room.suspects:
                    y = self.library_conservatory.top-self.library_conservatory.height/2
                    x = self.library_conservatory.right-3*(self.library_conservatory.width/4)
                    with self.library_conservatory.canvas.after:
                        Color(*self.COLORS[game_state.PEACOCK])
                        Ellipse(pos=(x-7.5, y-7.5), size=(15,15))
                if game_state.PLUM in room.suspects:
                    y = self.study_library.top-self.study_library.height/2
                    x = self.study_library.right-3*(self.study_library.width/4)
                    with self.study_library.canvas.after:
                        Color(*self.COLORS[game_state.PLUM])
                        Ellipse(pos=(x-7.5, y-7.5), size=(15,15))
                if game_state.GREEN in room.suspects:
                    y = self.conservatory_ballroom.top-3*(self.conservatory_ballroom.height/4)
                    x = self.conservatory_ballroom.right-self.conservatory_ballroom.width/2
                    with self.conservatory_ballroom.canvas.after:
                        Color(*self.COLORS[game_state.GREEN])
                        Ellipse(pos=(x-7.5, y-7.5), size=(15,15))
                if game_state.WHITE in room.suspects:
                    y = self.ballroom_kitchen.top-3*(self.ballroom_kitchen.height/4)
                    x = self.ballroom_kitchen.right-self.ballroom_kitchen.width/2
                    with self.ballroom_kitchen.canvas.after:
                        Color(*self.COLORS[game_state.WHITE])
                        Ellipse(pos=(x-7.5, y-7.5), size=(15,15))
                if game_state.MUSTARD in room.suspects:
                    y = self.lounge_dining.top-self.lounge_dining.height/2
                    x = self.lounge_dining.right-self.lounge_dining.width/4
                    with self.lounge_dining.canvas.after:
                        Color(*self.COLORS[game_state.MUSTARD])
                        Ellipse(pos=(x-7.5, y-7.5), size=(15,15))
            else:
                num_suspects = 0
                for suspect in room.suspects:
                    if ('hallway' in name):
                        y = tile.top-(tile.height/2)
                        x = tile.right-(tile.width/2)
                    else:
                        y = tile.top-(num_suspects/2+1)*(tile.height/4)
                        if num_suspects%2 == 0:
                            x = tile.right-2*(tile.width/3)
                        else:
                            x = tile.right-tile.width/3
                    with tile.canvas.after:
                        Color(*self.COLORS[suspect])
                        Ellipse(pos=(x-7.5, y-7.5), size=(15,15))
                    num_suspects += 1
                    
        # enable the game tiles if it's the user's turn, otherwise disable them
        if self.username == self.state.current_player.username:
            self.enable_tiles()
        else:
            self.disable_tiles()                    
        
    def make_move(self, room):
        try:
            self.suspect = self.client.get_player(self.username).suspect
            try:
                self.client.move_player(self.username, self.suspect, room)
                self.disable_tiles()
            except errors.GameClientException:
                p = ErrorPopup(message="Invalid move. Please select a valid Room or Hallway\nor end your turn.")
                p.open()
        except errors.GameClientException:
            p = ErrorPopup(message="Unable to obtain Player information from the Game Server. Please try again.")
            p.open()
        
class ControlPanel(FloatLayout):
    notifications = ObjectProperty(None)
    notepad = ObjectProperty(None)
    suggest_button = ObjectProperty(None)
    accuse_button = ObjectProperty(None)
    end_turn_button = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(ControlPanel, self).__init__(**kwargs)
        self.state = None
        self.player = None
        self.disproving = False

    def update(self, client, state, username):
        self.client = client
        self.state = state
        self.username = username
        
        try:
            self.player = self.client.get_player(self.username)
        except errors.GameClientException:
            print "ERROR: Could not get Player."

        # enable the game tiles if it's the user's turn, otherwise disable them
        if username == self.state.current_player.username:
            self.enable_buttons()
        else:
            self.disable_buttons()
            
        notifications = ''
        self.state.player_messages.reverse()
        for message in self.state.player_messages:
            notifications = notifications + message + '\n'
        self.notifications.text = notifications + '[ You are ' + self.username + ' (' + self.player.suspect + ') ]'
        
        notes = ''
        for card in self.player.game_cards:
            notes += card['item'] + " : " + card['item_type'] + '\n'
        for card in self.player.card_items_seen:
            notes += card['item'] + " : " + card['item_type'] + '\n'
        self.notepad.text = notes
        
        if self.state.suggestion_response_player == None or \
           (self.state.suggestion_response_player != None and \
           self.state.suggestion_response_player.username != self.username):
            self.disproving = False
        if self.state.suggestion_response_player != None and \
           self.state.suggestion_response_player.username == self.username and \
           not self.disproving:
            self.disproving = True
            self.disprove_suggestion_popup()
        '''content.add_widget(Label(text='You Win!'))
        content.add_widget(Label(text='Please continue playing.'))
        popup = Popup(content=content, title='Accusation Correct',
                      size_hint=(None, None), size=('300dp', '300dp'))'''
                
    def disable_buttons(self):
        self.suggest_button.disabled=True; self.suggest_button.canvas.opacity=.5
        self.accuse_button.disabled=True; self.accuse_button.canvas.opacity=.5
        self.end_turn_button.disabled=True; self.end_turn_button.canvas.opacity=.5
        
    def enable_buttons(self):
        self.suggest_button.disabled=False; self.suggest_button.canvas.opacity=1
        self.accuse_button.disabled=False; self.accuse_button.canvas.opacity=1
        self.end_turn_button.disabled=False; self.end_turn_button.canvas.opacity=1
        
    def disprove_suggestion_popup(self):
        cards = []
        try:
            self.player = self.client.get_player(self.username)
        except errors.GameClientException:
            print "ERROR: Could not get Player."
        for card in self.player.game_cards:
            if card['item'] == self.state.current_suggestion.suspect or \
               card['item'] == self.state.current_suggestion.weapon or \
               card['item'] == self.state.current_suggestion.room:
                cards += [card['item']]
        p = SuggestionResponsePopup(client=self.client, state=self.state, 
                                    username=self.username, cards=cards)
        p.open()
        
    def suggest_popup(self):
        p = SuggestionPopup(client=self.client, state=self.state)
        p.open()
        
    def accuse_popup(self):
        p = AccusationPopup(client=self.client, state=self.state)
        p.open()
        
    def end_turn(self):
        try:
            self.client.end_turn(self.username)
        except errors.GameClientException:
            p = ErrorPopup(message="Unable to end your turn. Please move your Suspect, \nmake a Suggestion, or try to end your turn again.")
            p.open()

class SuggestionResponsePopup(Popup):
    card = ObjectProperty(None)
    
    def __init__(self, client, state, username, cards, **kwargs):
        super(SuggestionResponsePopup, self).__init__(**kwargs)
        self.username = username
        self.client = client
        self.state = state
        self.card.values = cards
        
    def disprove_suggestion(self):
        try:
            self.client.make_suggestion_response(self.username, self.card.text)
            self.dismiss()
        except errors.GameClientException:
            p = ErrorPopup(message="Suggestion Response invalid. \nPlease select a valid Card and try again.")
            p.open()            
        
class AccusationPopup(Popup):
    suspect = ObjectProperty(None)
    weapon = ObjectProperty(None)
    room = ObjectProperty(None)

    def __init__(self, client, state, **kwargs):
        super(AccusationPopup, self).__init__(**kwargs)
        self.client = client
        self.state = state

    def confirm_popup(self):
        p = AccusationConfirmPopup(client=self.client, state=self.state, 
                                   suspect=self.suspect, weapon=self.weapon,
                                   room=self.room)
        p.open()
        self.dismiss()

class AccusationConfirmPopup(Popup):

    def __init__(self, client, state, suspect, weapon, room, **kwargs):
        super(AccusationConfirmPopup, self).__init__(**kwargs)
        self.client = client
        self.state = state
        self.suspect = suspect
        self.weapon = weapon
        self.room = room
        
    def make_accusation(self):
        try:
            self.client.make_accusation(self.state.current_player.username,
                                        self.suspect.text,
                                        self.weapon.text,
                                        self.room.text)
        except errors.GameClientException:
            p = ErrorPopup(message="Accusation invalid. Please select a valid Suspect, \nRoom, and Weapon, and try again.")
            p.open()            
        self.dismiss()
    
class SuggestionPopup(Popup):
    suspect = ObjectProperty(None)
    weapon = ObjectProperty(None)

    def __init__(self, client, state, **kwargs):
        super(SuggestionPopup, self).__init__(**kwargs)
        self.client = client
        self.state = state
    
    def make_suggestion(self):
        username = self.state.current_player.username
        for room in self.state.game_board.values():
            if self.state.current_player.suspect in room.suspects:
                break
        try:
            self.client.make_suggestion(username,
                                        self.suspect.text,
                                        self.weapon.text,
                                        room.name)
        except errors.GameClientException:
            p = ErrorPopup(message="You cannot make a Suggestion right now, or the Suspect \nor Weapon you chose for the Suggestion is invalid.\nPlease try again.")
            p.open()            
            
        self.dismiss()

class ErrorPopup(Popup):
    message = ObjectProperty(None)

    def __init__(self, message, **kwargs):
        super(ErrorPopup, self).__init__(**kwargs)
        self.message.text = message
    
class CluelessApp(App):

    def build(self):
        client = game_play.GameClient(host="127.0.0.1", port="5000")
        root = ScreenManager()
        root.transition = WipeTransition()
        root.add_widget(StartScreen(client, name="start"))
        root.add_widget(GameScreen(client, name="game"))
        return root

if __name__ == '__main__':
    CluelessApp().run()
