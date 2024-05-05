from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from random import randint
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.video import Video

import cam
from threading import Thread
from pathlib import Path
import webbrowser
Window.size = (300, 650)
Window.clearcolor = (255/255, 186/255, 3/255, 1)
Window.title = "App"
min_time = [0, 0]
max_time = [0, 0]
reps = 0

def camer():
    cam.Camera()
    
th = Thread(target=camer)
th.start()

class ScreenMain(Screen):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        float_layout = FloatLayout()

        self.timeTXT_label = Label(text="Интервал", pos_hint={"x":0, "y":.25})
        float_layout.add_widget(self.timeTXT_label)
        self.time_label = Label(text=f"{min_time[0]}min {min_time[1]}sec - {max_time[0]}min {max_time[1]}sec", pos_hint={"x":0, "y":.2})
        float_layout.add_widget(self.time_label)

        self.progressbar = ProgressBar(value=50, pos_hint={"x":0, "y":-.4})


        float_layout.add_widget(self.progressbar)
        self.repsTXT_label = Label(text=f"Повторы", pos_hint={"x":0, "y":.1})
        float_layout.add_widget(self.repsTXT_label)
        self.reps_label = Label(text=f"{reps}", pos_hint={"x":0, "y":.05})
        float_layout.add_widget(self.reps_label)

        self.btn_start = Button(text="Начать\n упражнение", size_hint=(0.4, 0.13),  on_press=self._on_press_button_start,  pos_hint={"x":.05, "y":.2}, background_color = (96/255, 133/255, 2/255, 1))
        float_layout.add_widget(self.btn_start)
        self.btn_stop = Button(text="Завершить \n упражнение",  on_press=self._on_press_button_stop, size_hint=(0.4, 0.13),  pos_hint={"x":.55, "y":.2}, background_color = (96/255, 133/255, 2/255, 1))
        float_layout.add_widget(self.btn_stop)
        self.btn_settings = Button(text="Редактировать",  on_press=self._on_press_button_settings, size_hint=(0.4, 0.1), pos_hint={"x":.3, "y":.4}, background_color = (96/255, 133/255, 2/255, 1))
        float_layout.add_widget(self.btn_settings)
        self.add_widget(float_layout)

        Clock.schedule_interval(self.updateBar, 0.5)

    def _on_press_button_start(self, *args):
        self.manager.current = 'stress'
        

    def _on_press_button_stop(self, *args):
        pass

    def _on_press_button_settings(self, *args):
        self.manager.current = 'settings'
        
    def updateBar(self, *args):
        if self.progressbar.value != int(Path('global.txt').read_text())//2:
            self.progressbar.value= int(Path('global.txt').read_text())//2
        print(self.progressbar.value , "," , int(Path('global.txt').read_text())//2)
        self.reps_label.text = f"{reps}"
        self.time_label.text = f"{min_time[0]}min {min_time[1]}sec - {max_time[0]}min {max_time[1]}sec"

class ScreenSettings(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        float_layout = FloatLayout()
        self.timeTXT_label = Label(text="Интервал", pos_hint={"x":0, "y":.3})
        float_layout.add_widget(self.timeTXT_label)
        self.time1_label = Label(text=f"min", pos_hint={"x":-.4, "y":.24})
        float_layout.add_widget(self.time1_label)
        self.time2_label = Label(text=f"max", pos_hint={"x":.4, "y":.24})
        float_layout.add_widget(self.time2_label)

        self.repsTXT_label = Label(text=f"Повторы", pos_hint={"x":0, "y":.1})
        float_layout.add_widget(self.repsTXT_label)
        self.min_min_input = TextInput(multiline=False, size_hint=(0.1, 0.05),pos_hint={"x":.2, "y":.72})
        float_layout.add_widget(self.min_min_input)
        self.min_sec_input = TextInput(multiline=False, size_hint=(0.1, 0.05),pos_hint={"x":.3, "y":.72})
        float_layout.add_widget(self.min_sec_input)
        self.max_min_input = TextInput(multiline=False, size_hint=(0.1, 0.05),pos_hint={"x":.6, "y":.72})
        float_layout.add_widget(self.max_min_input)
        self.max_sec_input = TextInput(multiline=False, size_hint=(0.1, 0.05),pos_hint={"x":.7, "y":.72})
        float_layout.add_widget(self.max_sec_input)
        self.rep_input = TextInput(multiline=False, size_hint=(0.1, 0.05),pos_hint={"x":.45, "y":.5})
        float_layout.add_widget(self.rep_input)

        self.btn_settings = Button(text="Сохранить",  on_press=self._on_press_button_settings, size_hint=(0.4, 0.1), pos_hint={"x":.3, "y":.33}, background_color = (96/255, 133/255, 2/255, 1))
        float_layout.add_widget(self.btn_settings)
        self.add_widget(float_layout)


    def _on_press_button_settings(self, *args):
        self.manager.current = 'main_screen'
        global min_time 
        global max_time 
        global reps

        min_time = [self.min_min_input.text, self.min_sec_input.text]
        max_time = [self.max_min_input.text, self.max_sec_input.text]
        reps = self.rep_input.text
    
    def updateBar(self, *args):
        if self.progressbar.value != int(Path('global.txt').read_text())//2:
            self.progressbar.value= int(Path('global.txt').read_text())//2




class ScreenStress(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        float_layout = FloatLayout()

        self.timeTXT_label = Label(text="Интервал", pos_hint={"x":0, "y":.25})
        float_layout.add_widget(self.timeTXT_label)
        self.time_label = Label(text=f"{min_time[0]}min {min_time[1]}sec - {max_time[0]}min {max_time[1]}sec", pos_hint={"x":0, "y":.2})
        float_layout.add_widget(self.time_label)
        self.progressbar = ProgressBar(value=50, pos_hint={"x":0, "y":-.4})
        float_layout.add_widget(self.progressbar)
        self.repsTXT_label = Label(text=f"Повторы", pos_hint={"x":0, "y":.1})
        float_layout.add_widget(self.repsTXT_label)
        self.reps_label = Label(text=f"{reps}", pos_hint={"x":0, "y":.05})
        float_layout.add_widget(self.reps_label)
        self.btn_settings = Button(text="Not for realise",  on_press=self.final, size_hint=(0.4, 0.1), pos_hint={"x":.35, "y":.4}, background_color = (96/255, 133/255, 2/255, 1))

        float_layout.add_widget(self.btn_settings)
        self.add_widget(float_layout)
        Clock.schedule_interval(self.updateBar, 0.5)

    def final(self, *args):
        self.manager.current = 'final'
    
    def updateBar(self, *args):
        if self.progressbar.value != int(Path('global.txt').read_text())//2:
            self.progressbar.value= int(Path('global.txt').read_text())//2
        print(self.progressbar.value , "," , int(Path('global.txt').read_text())//2)

        self.reps_label.text = f"{reps}"
        self.time_label.text = f"{min_time[0]}min {min_time[1]}sec - {max_time[0]}min {max_time[1]}sec"





class ScreenFinal(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        float_layout = FloatLayout()


        self.btn_settings = Button(text="В главное меню",  on_press=self._on_press_button_settings, size_hint=(0.4, 0.1), pos_hint={"x":.3, "y":.4}, background_color = (96/255, 133/255, 2/255, 1))

        float_layout.add_widget(self.btn_settings)
        self.add_widget(float_layout)
        
    def _on_press_button_settings(self, *args):
        self.manager.current = 'main_screen'

class NoStressApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ScreenMain(name='main_screen'))
        sm.add_widget(ScreenSettings(name='settings'))
        sm.add_widget(ScreenStress(name='stress'))
        sm.add_widget(ScreenFinal(name='final'))
        return sm



if __name__ == "__main__":
    NoStressApp().run()