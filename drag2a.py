#!/usr/bin/env python3

"""
Use touch events to drag a rectangle around the screen with borders.
"""

from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder

kv = """
<Rect>:
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            size: self.size
            pos: self.x,self.y

<DragRect>:
    drag_rectangle: self.x, self.y, self.width, self.height

<MyLabel>:
    background_color: 0.5,0.5,0.5,1
    color: 0,0,0,1
    padding: 10, 10

<Box>:
    pos: 100, 100
    size_hint: None, None
    size: 50,50
    background_color: 0,1,0,0.5

BoxLayout:
    orientation: "horizontal"
    MyLabel:
        text: "Left"
        size_hint_x: None
        width: self.texture_size[0]
    BoxLayout:
        orientation: "vertical"
        MyLabel:
            text: "Top"
            size_hint_y: None
            height: self.texture_size[1]
        RelativeLayout:
            id: page
        MyLabel:
            text: "Bottom"
            size_hint_y: None
            height: self.texture_size[1]
    MyLabel:
        text: "Right"
        size_hint_x: None
        width: self.texture_size[0]
"""

# mixin class
class Rect:
    background_color = ListProperty([1, 1, 1, 1])

# Similar to DragBehavior
class DragRect(Rect, FloatLayout):
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

class RectLabel(Rect, Label):
    pass

class MyLabel(RectLabel):
    pass

class Box(DragRect):
    pass

class TestApp(App):
    def build(self):
        root = Builder.load_string(kv)
        page = root.ids.page
        page.add_widget(Box())
        return root
    
TestApp().run()
