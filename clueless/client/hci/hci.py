import kivy
kivy.require('1.1.3')

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner

class StartScreen(Screen):
    pass

class GameScreen(Screen):
    pass

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
#        content.add_widget(Label(text='You Win!'))
#        content.add_widget(Label(text='Please continue playing.'))
#        popup = Popup(content=content, title='Accusation Correct',
#                      size_hint=(None, None), size=('300dp', '300dp'))

class SuggestionPopup(Popup):
    pass

class Gameboard(FloatLayout):

    value = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Gameboard, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30.)

    def update(self, dt):
        self.value += dt

class InstrumentPanel(FloatLayout):

    value = NumericProperty(0)

    def __init__(self, **kwargs):
        super(InstrumentPanel, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30.)

    def update(self, dt):
        self.value += dt
        
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

class CluelessApp(App):

    def build(self):
        root = ScreenManager()
        root.transition = WipeTransition()
        root.add_widget(StartScreen(name="start"))
        root.add_widget(GameScreen(name="game"))
        return root

if __name__ == '__main__':
    CluelessApp().run()
