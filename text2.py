#!/usr/bin/env python3

"""
Test of minimum-size text labels with an outline.
"""

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ListProperty
from kivy.app import App
from kivy.lang import Builder

kv = """
<MyLabel>:
    size_hint: None, None
    size: self.texture_size
    padding: 5, 5
    halign: 'center'
    valign: 'middle'

<RectLabel>:
    canvas.before:
        Color:
            rgba: 1.0,0.0,0.0,0.5
        Rectangle:
            size: self.size
            pos: self.pos

<Symbol>:
    size_hint: None, None
    width: box.width + 2*self.outline_width
    height: box.height + 2*self.outline_width
    canvas:
        Color:
            rgba: 0.0,0.0,1.0,0.5
        RoundedRectangle:
            size: self.width-self.outline_width, self.height-self.outline_width
            pos: self.x+self.outline_width/2.0,self.y+self.outline_width/2.0
            radius: (self.radius,)
        Color:
            rgba: 1.0,1.0,1.0,0.5
        Line:
            rounded_rectangle: self.x + self.outline_width/2.0, \
                               self.y + self.outline_width/2.0, \
                               self.width - self.outline_width, \
                               self.height - self.outline_width, self.radius
            width: self.outline_width/2.0 # actually = outline_width
    GridLayout:
        id: box
        cols: 1
        x: root.x + root.outline_width
        y: root.y + root.outline_width
        size_hint: None, None
        size: self.minimum_size
        MyLabel:
            text: "text1"
        MyLabel:
            text: "text2"
        MyLabel:
            text: "text3"
        RectLabel:
            text: "text4"

ScatterLayout:
    Symbol:
    Symbol:
        outline_width: 12
        pos: 300, 300
"""

class MyLabel(Label):
    pass

class RectLabel(MyLabel):
    pass

class Symbol(FloatLayout):
    outline_width = NumericProperty(4.0)
    radius = NumericProperty(10.0)
    
class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

TestApp().run()
