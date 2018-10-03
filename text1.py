#!/usr/bin/env python3

"""
Test of minimum-size text labels.
"""

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder

kv = """
<MyLabel>:
    size_hint: None, None
    size: self.texture_size
    padding: 5, 5
    halign: 'center'
    valign: 'middle'
    canvas.before:
        Color:
            rgba: 1.0,0.0,0.0,.5
        Rectangle:
            size: self.size
            pos: self.pos

<Symbol>:
    size_hint: None, None
    size: box.size
    canvas:
        Color:
            rgba: 0.0,0.0,1.0,.5
        Rectangle:
            size: self.size
            pos: self.pos
    BoxLayout:
        id: box
        orientation: "vertical"
        x: root.x
        y: root.y
        size_hint: None, None
        size: self.minimum_size
        MyLabel:
            text: "text1"
        MyLabel:
            text: "text2"
        MyLabel:
            text: "text3"
        MyLabel:
            text: "text4"

FloatLayout:
    Symbol:
    Symbol:
        pos: 300, 300
"""

class MyLabel(Label):
    pass

class Symbol(FloatLayout):
    pass

class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

TestApp().run()
