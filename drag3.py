#!/usr/bin/env python3

"""
Use DragBehavior mixin class to drag a rectangle around the screen with
borders, keeping the rectangle inside its parent widget.
"""

from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.uix.behaviors import DragBehavior
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

class DragRect(DragBehavior, Rect, FloatLayout):
    def on_pos(self, *largs):
        # Parent does not exist when created
        if self.parent is None:
            return
        
        if self.x < 0:
            self.x = 0
        elif self.right > self.parent.width:
            self.right = self.parent.width

        if self.y < 0:
            self.y = 0
        elif self.top > self.parent.height:
            self.top = self.parent.height

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
