#!/usr/bin/env python3

from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder

kv = """
<DragRect>:
    drag_rectangle: self.x, self.y, self.width, self.height
    pos: 100, 100
    size_hint: None, None
    size: 50,50
    canvas:
        Color:
            rgba: 0,0,1,.5
        Rectangle:
            size: self.size
            pos: self.x,self.y

FloatLayout:
    DragRect
"""

class DragRect(DragBehavior, FloatLayout):
    pass

class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

TestApp().run()
