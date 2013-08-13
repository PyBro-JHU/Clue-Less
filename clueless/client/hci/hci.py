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
from kivy.uix.spinner import Spinner

from clueless.client import game_play
from clueless.model import game_state

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
            
class GamePiece(Widget):
    pass

class GameTile(DisableButton, Widget):
    pass

class StartScreen(Screen):
    username = ObjectProperty(None)
    suspect = ObjectProperty(None)
    
    def __init__(self, client, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.client = client
        
    def register_player(self):
        self.client.register_player(self.username.text)
        self.client.choose_suspect(self.username.text, self.suspect.text)
        self.manager.get_screen('game').username = self.username.text
        self.manager.current = self.manager.next()

class GameScreen(Screen):
    state = game_state.GameState(
                game_id="12345",
                players=[game_state.Player(
                            username="testuser1",
                            suspect=game_state.PLUM,
                            game_cards=[game_state.GameCard(
                                            item=game_state.WRENCH,
                                            item_type=game_state.WEAPON)]),
                         game_state.Player(
                            username="testuser2",
                            suspect=game_state.PEACOCK,
                            game_cards=[game_state.GameCard(
                                            item=game_state.REVOLVER,
                                            item_type=game_state.WEAPON)])
        ])
    gameboard = ObjectProperty(0)
    controls = ObjectProperty(0)
    
    def __init__(self, client, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.client = client
        self.username=''
        #self.state = self.client.start_new_game()
        Clock.schedule_interval(self.update, 1 / 30.)

    def update(self, dt):
        self.gameboard.update(self.client, 
                              self.state.format()["game_id"],
                              self.username)
        self.controls.update(self.client, 
                             self.state.format()["game_id"],
                             self.username)

class Gameboard(FloatLayout):
    scarlet = ObjectProperty(None)
    mustard = ObjectProperty(None)
    plum = ObjectProperty(None)
    green = ObjectProperty(None)
    white = ObjectProperty(None)
    peacock = ObjectProperty(None)
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

    def __init__(self, **kwargs):
        super(Gameboard, self).__init__(**kwargs)
        
    def disable_tiles(self):
        self.study.disabled=True; self.study_hall.disabled=True
        self.hall.disabled=True; self.hall_lounge.disabled=True
        self.lounge.disabled=True; self.study_library.disabled=True
        self.study_billiard.disabled=True; self.hall_billiard.disabled=True
        self.lounge_billiard.disabled=True; self.lounge_dining.disabled=True
        self.library.disabled=True; self.library_billiard.disabled=True
        self.billiard_room.disabled=True; self.billiard_dining.disabled=True
        self.dining_room.disabled=True; self.library_conservatory.disabled=True
        self.conservatory_billiard.disabled=True; self.billiard_ballroom.disabled=True
        self.kitchen_billiard.disabled=True; self.dining_kitchen.disabled=True
        self.conservatory.disabled=True; self.conservatory_ballroom.disabled=True
        self.ballroom.disabled=True; self.ballroom_kitchen.disabled=True
        self.kitchen.disabled=True;

    def enable_tiles(self):
        self.study.disabled=False; self.study_hall.disabled=False
        self.hall.disabled=False; self.hall_lounge.disabled=False
        self.lounge.disabled=False; self.study_library.disabled=False
        self.study_billiard.disabled=False; self.hall_billiard.disabled=False
        self.lounge_billiard.disabled=False; self.lounge_dining.disabled=False
        self.library.disabled=False; self.library_billiard.disabled=False
        self.billiard_room.disabled=False; self.billiard_dining.disabled=False
        self.dining_room.disabled=False; self.library_conservatory.disabled=False
        self.conservatory_billiard.disabled=False; self.billiard_ballroom.disabled=False
        self.kitchen_billiard.disabled=False; self.dining_kitchen.disabled=False
        self.conservatory.disabled=False; self.conservatory_ballroom.disabled=False
        self.ballroom.disabled=False; self.ballroom_kitchen.disabled=False
        self.kitchen.disabled=False

    def update(self, client, game_id, username):
        self.client = client
        self.username = username
        '''self.state = self.client.get_game_state(game_id)
        if username == self.state.current_player.format['username']:
            self.enable_tiles()
        else:
            self.disable_tiles()
        for room in self.state.game_board:
            if room.name in game_state.SUSPECTS:
                if room.suspects[0] == game_state.SCARLET:
                    self.scarlet.center_y = self.hall_lounge.top-self.hall_lounge.height/4
                    self.scarlet.center_x = self.hall_lounge.right-self.hall_lounge.width/2
                if room.suspects[0] == game_state.PEACOCK:
                    self.peacock.center_y = self.library_conservatory.top-self.library_conservatory.height/2
                    self.peacock.center_x = self.library_conservatory.right-3*(self.library_conservatory.width/4)
                if room.suspects[0] == game_state.PLUM:
                    self.plum.center_y = self.study_library.top-self.study_library.height/2
                    self.plum.center_x = self.study_library.right-3*(self.study_library.width/4)
                if room.suspects[0] == game_state.GREEN:
                    self.green.center_y = self.conservatory_ballroom.top-3*(self.conservatory_ballroom.height/4)
                    self.green.center_x = self.conservatory_ballroom.right-self.conservatory_ballroom.width/2
                if room.suspects[0] == game_state.WHITE:
                    self.white.center_y = self.ballroom_kitchen.top-3*(self.ballroom_kitchen.height/4)
                    self.white.center_x = self.ballroom_kitchen.right-self.ballroom_kitchen.width/2
                if room.suspects[0] == game_state.MUSTARD:
                    self.mustard.center_y = self.lounge_dining.top-self.lounge_dining.height/2
                    self.mustard.center_x = self.lounge_dining.right-self.lounge_dining.width/4
            else:
                num_suspects = 0
                for suspect in room.suspects:
                    if suspect == game_state.SCARLET:
                        my_suspect = self.scarlet
                    if suspect == game_state.PEACOCK:
                        my_suspect = self.peacock
                    if suspect == game_state.PLUM:
                        my_suspect = self.plum
                    if suspect == game_state.GREEN:
                        my_suspect = self.green
                    if suspect == game_state.WHITE:
                        my_suspect = self.white
                    if suspect == game_state.MUSTARD:
                        my_suspect = self.mustard
                    my_suspect.parent.remove_widget(my_suspect)
                    # need to translate room.name for my_room (hard-coded to conservatory)
                    my_room = self.conservatory
                    my_room.add_widget(my_suspect)
                    my_suspect.center_y = my_room.top-(num_suspects/2+1)*(my_room.height/4)
                    if num_suspects%2 == 0:
                        my_suspect.center_x = self.my_room.right-2*(my_room.width/3)
                    else:
                        my_suspect.center_x = self.my_room.right-my_room.width/3
                    num_suspects += 1'''

        self.scarlet.parent.remove_widget(self.scarlet)
        self.hall_lounge.add_widget(self.scarlet)
        self.scarlet.center_y = self.hall_lounge.top-self.hall_lounge.height/4
        self.scarlet.center_x = self.hall_lounge.right-self.hall_lounge.width/2
        
        self.peacock.parent.remove_widget(self.peacock)
        self.library_conservatory.add_widget(self.peacock)
        self.peacock.center_y = self.library_conservatory.top-self.library_conservatory.height/2
        self.peacock.center_x = self.library_conservatory.right-3*(self.library_conservatory.width/4)
        
        self.plum.parent.remove_widget(self.plum)
        self.study_library.add_widget(self.plum)
        self.plum.center_y = self.study_library.top-self.study_library.height/2
        self.plum.center_x = self.study_library.right-3*(self.study_library.width/4)
        
        self.green.parent.remove_widget(self.green)
        self.conservatory_ballroom.add_widget(self.green)
        self.green.center_y = self.conservatory_ballroom.top-3*(self.conservatory_ballroom.height/4)
        self.green.center_x = self.conservatory_ballroom.right-self.conservatory_ballroom.width/2
        
        self.white.parent.remove_widget(self.white)
        self.ballroom_kitchen.add_widget(self.white)
        self.white.center_y = self.ballroom_kitchen.top-3*(self.ballroom_kitchen.height/4)
        self.white.center_x = self.ballroom_kitchen.right-self.ballroom_kitchen.width/2
        
        self.mustard.parent.remove_widget(self.mustard)
        self.lounge_dining.add_widget(self.mustard)
        self.mustard.center_y = self.lounge_dining.top-self.lounge_dining.height/2
        self.mustard.center_x = self.lounge_dining.right-self.lounge_dining.width/4
        
    def debug(self):
        import pdb; pdb.set_trace()

class ControlPanel(FloatLayout):
    notifications = ObjectProperty(None)
    notepad = ObjectProperty(None)
    suggest = ObjectProperty(None)
    accuse = ObjectProperty(None)
    end_turn = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(ControlPanel, self).__init__(**kwargs)

    def update(self, client, game_id, username):
        self.client = client
        self.username = username
        '''self.state = self.client.get_game_state(game_id)
        self.notifications.text = self.state.player_messages
        notes = ''
        for card in client.get_player(self.username).game_cards:
            notes += card.item, ":", card.type
        for card in client.get_player(self.username).card_items_seen:
            notes += card.item, ":", card.type
        self.notepad.text = notes
        if username == self.state.current_player.format['username']:
            self.enable_buttons()
        else:
            self.disable_buttons()'''
                
    def disable_buttons(self):
        self.suggest.disabled=True
        self.accuse.disabled=True
        self.end_turn.disabled=True
        
    def enable_buttons(self):
        self.suggest.disabled=False
        self.accuse.disabled=False
        self.end_turn.disabled=False
        
    def suggest_popup(self):
        p = SuggestionPopup()
        p.open()
        
    def disprove_suggestion_popup(self):
        btnclose = Button(text='Submit', size_hint_y=None, height='50sp')
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='Miss Scarlet suggested Colonel \nMustard in Library with Revolver.'))
        content.add_widget(Label(text='Select card to prove false'))
        spinner = Spinner(text='Card',
                          values=('Knife', 'Library'),
                          size_hint=(None, None), size=(100, 44),
                          pos_hint={'center_x': .5, 'center_y': .5})
        content.add_widget(spinner)
        content.add_widget(btnclose)
        popup = Popup(content=content, title='Prove Suggestion False',
                      size_hint=(None, None), size=('300dp', '300dp'))
        btnclose.bind(on_release=popup.dismiss)
        popup.open()

    def accuse_popup(self):
        p = AccusationPopup()
        p.open()

class AccusationPopup(Popup):
    
    def confirm_popup(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='Are you sure you want to make an Accusation?'))
        accuseButton = Button(text='Accuse', size_hint_y=None, height='50sp')
        cancelButton = Button(text='Cancel', size_hint_y=None, height='50sp')
        content.add_widget(accuseButton)
        content.add_widget(cancelButton)
        popup = Popup(content=content, title='Make Accusation?', auto_dismiss=False,
                      size_hint=(None, None), size=('500dp', '300dp'))
        cancelButton.bind(on_release=popup.dismiss)
        accuseButton.bind(on_release=popup.dismiss)
        popup.open()
        '''content.add_widget(Label(text='You Win!'))
        content.add_widget(Label(text='Please continue playing.'))
        popup = Popup(content=content, title='Accusation Correct',
                      size_hint=(None, None), size=('300dp', '300dp'))'''

class SuggestionPopup(Popup):
    pass

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
