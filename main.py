import os
import random
import time

import kivy
from  kivy.app import App

from kivy.uix.label import Label
from kivy.uix.image import Image

from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp

from kivy.core.audio import  SoundLoader

from kivy.core.window import Window

from kivy.clock import  Clock

from kivy.uix.progressbar import ProgressBar

from kivy.uix.slider import Slider
from kivy.uix.switch import Switch

Window.size=(400,600)

class MyApp(MDApp):
    def build(self):

        layout= MDRelativeLayout(md_bg_color = [1,0,0,1])

        self.music_dir="M:/FAV SONGS"

        self.music_files= os.listdir(self.music_dir)

        self.song_list=[x for x in self.music_files if x.endswith(('mp3'))]

        self.song_count=len(self.song_list)

        self.song_lable=Label(pos_hint={'center_x':0.5,'center_y':0.96},
                              size_hint=(1,1),
                              font_size=18)
        
        self.albumimage= Image(pos_hint={'center_x':0.5,'center_y':0.55},
                              size_hint=(0.8,0.75))
        
        self.currentTime =Label(text ="00:00",
                                pos_hint ={'center_x':.16,'center_y':.145},
                                size_hint=(1,1),
                                font_size=18)
        
        self.totalTime =Label(text ="00:00",
                                pos_hint ={'center_x':.84,'center_y':.145},
                                size_hint=(1,1),
                                font_size=18)
        
        self.progressbar = ProgressBar(max=100,
                                       value=0,
                                       pos_hint ={'center_x':0.5,'center_y':0.12},
                                       size_hint=(.8,.75))
        
        self.volumeslider = Slider(min=0,
                                   max=1,
                                   value=0.5,
                                   orientation='horizontal',
                                   pos_hint ={'center_x':0.2,'center_y':0.05},
                                   size_hint=(0.2,0.2))

        self.playbutton=MDIconButton(pos_hint={'center_x':0.4,'center_y':0.05},
                                     icon='play.png',
                                     on_press=self.playaudio )

        self.stopbutton=MDIconButton(pos_hint={'center_x':0.55,'center_y':0.05},
                                     icon='stop.png',
                                     on_press=self.stopaudio, disabled=True )

        layout.add_widget(self.playbutton)
        layout.add_widget(self.stopbutton)
        layout.add_widget(self.song_lable)
        layout.add_widget(self.albumimage)

        layout.add_widget(self.currentTime)
        layout.add_widget(self.totalTime)
        layout.add_widget(self.progressbar)

        layout.add_widget(self.volumeslider)

        Clock.schedule_once(self.playaudio)

        def volume(instance, value):
            self.sound.volume=value

        self.volumeslider.bind(value=volume)

        return layout
    
    def playaudio(self,obj):
        self.playbutton.disabled=True
        self.stopbutton.disabled=False
        self.song_title=self.song_list[random.randrange(0,self.song_count)]
        self.sound= SoundLoader.load('{}/{}'.format(self.music_dir,self.song_title))

        self.song_lable.text= self.song_title[0:-4]
        self.albumimage.source=self.song_title[0:-4]+".jpg"

        self.sound.play()

        self.progressbarEvent=Clock.schedule_interval(self.updateprogressbar,self.sound.length/60)
        self.settimeEvent = Clock.schedule_interval(self.settime,1)

    def stopaudio(self,obj):
        self.playbutton.disabled=False
        self.stopbutton.disabled=True
        self.sound.stop()

        self.progressbarEvent.cancel()
        self.settimeEvent.cancel()
        self.progressbar.value=0
        self.currentTime.text="00:00"
        self.totalTime.text="00:00"

    def updateprogressbar(self,value):
        if self.progressbar.value <100:
            self.progressbar.value += 1   
    
    def settime(self, dt):
        # Calculate the current time based on the progress bar value
        current_time_seconds = (self.progressbar.value / 100) * self.sound.length
        current_time = time.strftime('%M:%S', time.gmtime(current_time_seconds))
        
        # Get the total time of the song
        total_time = time.strftime('%M:%S', time.gmtime(self.sound.length))

        self.currentTime.text = current_time
        self.totalTime.text = total_time
    
if __name__=='__main__':
    MyApp().run()
    

