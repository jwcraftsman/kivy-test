#!/usr/bin/env python3

"""
Drawing canvas rectangles.
"""

from kivy.app import App
from kivy.lang import Builder

kv = """
ScatterLayout:
    canvas:
        Color:
            rgba: 0.0,0.0,1.0,.5
        Rectangle:
            size: 100, 100
            pos: 0, 0
        Rectangle:
            size: 100, 100
            pos: 0, 200
        Color:
            rgba: 1.0,0.0,0.0,0.5
        Line:
            rectangle: 0, 0, 100, 100
            # Note that the actual width is 50, not 25
            width: 25
        Line:
            rectangle: 12.5, 212.5, 100-25, 100-25
            # Note that the actual width is 25, not 12.5
            width: 12.5
"""

class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

TestApp().run()
