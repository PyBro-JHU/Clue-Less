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
from kivy.graphics import Ellipse, Color

from clueless.client import game_play
from clueless.client import errors
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
        self.manager.get_screen('game').start_game(self.username.text)
        self.manager.current = self.manager.next()

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
        self.state = self.client.start_new_game()
        self.game_id = self.state.game_id

    def update(self, dt):
        if self.state != None:
            self.gameboard.update(self.client, 
                                  self.state.game_id,
                                  self.username)
            self.controls.update(self.client, 
                                 self.state.game_id,
                                 self.username)
        
    def quit_game(self):
        self.state=None
        self.client.destroy_game(self.game_id)
        self.manager.current = self.manager.previous()

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
        
    def disable_tiles(self):
        self.study.disabled=True; self.study.canvas.opacity=.5
        self.study_hall.disabled=True
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
        self.state = self.client.get_game_state(game_id)
        if username == self.state.current_player.username:
            self.enable_tiles()
        else:
            self.disable_tiles()
        for name, room in self.state.game_board.iteritems():
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
                    # need to translate name for my_room (hard-coded to conservatory)
                    my_room = self.conservatory
                    y = my_room.top-(num_suspects/2+1)*(my_room.height/4)
                    if num_suspects%2 == 0:
                        x = self.my_room.right-2*(my_room.width/3)
                    else:
                        x = self.my_room.right-my_room.width/3
                    with self.my_room.canvas.after:
                        Color(*self.COLORS[suspect])
                        Ellipse(pos=(x-7.5, y-7.5), size=(15,15))
                    num_suspects += 1
                    
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
        self.state = self.client.get_game_state(game_id)
        notifications = ''
        for note in self.state.player_messages:
            notifications = notifications + note + '\n'
        self.notifications.text = notifications
        notes = ''
        for card in client.get_player(self.username).game_cards:
            notes += card['item'] + " : " + card['item_type'] + '\n'
        for card in client.get_player(self.username).card_items_seen:
            notes += card['item'] + " : " + card['item_type'] + '\n'
        self.notepad.text = notes
        if username == self.state.current_player.username:
            self.enable_buttons()
        else:
            self.disable_buttons()
                
    def disable_buttons(self):
        self.suggest.disabled=True; self.suggest.canvas.opacity=.5
        self.accuse.disabled=True; self.accuse.canvas.opacity=.5
        self.end_turn.disabled=True; self.end_turn.canvas.opacity=.5
        
    def enable_buttons(self):
        self.suggest.disabled=False; self.suggest.canvas.opacity=1
        self.accuse.disabled=False; self.accuse.canvas.opacity=1
        self.end_turn.disabled=False; self.end_turn.canvas.opacity=1
        
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
