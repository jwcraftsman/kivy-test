#!/usr/bin/env python3

"""
Use touch events to drag a rectangle around the screen.
"""

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

# Similar to DragBehavior
class DragRect(FloatLayout):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True # Don't allow simultaneous grabs
        
    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.x += touch.dx
            self.y += touch.dy
                
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)

class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

TestApp().run()
