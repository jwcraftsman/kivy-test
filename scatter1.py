#!/usr/bin/env python3

"""
Use touch to pan and "pinch" to zoom on the ScatterLayout.  The ScatterLayout
is listed first and a placeholder is used for sizing/positioning to keep
the ScatterLayout above the other widgets.
"""

from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.scatterlayout import ScatterLayout
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

<MyLabel>:
    background_color: 0.5,0.5,0.5,1
    color: 0,0,0,1
    padding: 10, 10

<Box>:
    pos: 100, 100
    size_hint: None, None
    size: 50,50
    background_color: 0,1,0,0.5

FloatLayout:
    MyScatterLayout:
        placeholder: placeholder
        auto_bring_to_front: 0
        do_rotation: 0
        scale_min: 1.0
        size_hint: None, None
        size: self.placeholder.size
        pos: self.placeholder.pos
        canvas.before:
            Color:
                rgba: 1,0,0,1
            Rectangle:
                size: self.size
            Color:
                rgba: .05,.05,.2,1
            Rectangle:
                size: self.width - 10, self.height - 10
                pos: 5, 5
        Box:
        Box:
            pos: 100, 200
            background_color: 0,0,1,0.5
        Box:
            pos: 400, 400
            background_color: 1,0,1,0.5
    BoxLayout:
        orientation: "horizontal"
        size: root.size
        pos: root.pos
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
            FloatLayout:
                id: placeholder
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

class RectLabel(Rect, Label):
    pass

class MyLabel(RectLabel):
    pass

class Box(Rect, Widget):
    pass

class MyScatterLayout(ScatterLayout):
    placeholder = ObjectProperty(None)
    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        if touch.grab_current is self:
            if self.x > self.placeholder.x:
                self.x = self.placeholder.x
            if self.y > self.placeholder.y:
                self.y = self.placeholder.y
            if self.right < self.placeholder.right:
                self.right = self.placeholder.right
            if self.top < self.placeholder.top:
                self.top = self.placeholder.top
            return
        
class TestApp(App):
    def build(self):
        root = Builder.load_string(kv)
        return root
    
TestApp().run()
