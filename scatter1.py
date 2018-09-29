#!/usr/bin/env python3

"""
Use touch drags to pan and "pinch" to zoom on the ScatterLayout.
The ScatterLayout is listed first and a placeholder is used for
sizing/positioning to keep the ScatterLayout below the other widgets.
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
        placeholder_size: placeholder.size
        auto_bring_to_front: 0
        do_rotation: 0
        scale_min: self.get_min_scale(self.placeholder.width,self.placeholder.height)
        size_hint: None, None
        size: 500, 500
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
    placeholder_size = ListProperty([10,10])
    def on_placeholder_size(self, width, height):
        if self.scale < self.scale_min:
            self.scale = self.scale_min
        self.keep_in_bounds()
        
    def on_transform_with_touch(self, touch):
        self.keep_in_bounds()
        
    def keep_in_bounds(self):
        if self.width*self.scale >= self.placeholder.width:
            if self.x > self.placeholder.x:
                self.x = self.placeholder.x
            if self.x + self.width*self.scale < self.placeholder.right:
                self.x = self.placeholder.right - self.width*self.scale
        else:
            self.x = self.placeholder.x + (self.placeholder.width -
                                           self.width*self.scale)/2
        if self.height*self.scale >= self.placeholder.height:
            if self.y > self.placeholder.y:
                self.y = self.placeholder.y
            if self.y + self.height*self.scale < self.placeholder.top:
                self.y = self.placeholder.top - self.height*self.scale
        else:
            self.y = self.placeholder.y + (self.placeholder.height -
                                           self.height*self.scale)/2
        return

    def get_min_scale(self, w, h):
        min_x_scale = self.placeholder.width/self.width
        min_y_scale = self.placeholder.height/self.height
        #print(min_x_scale, min_y_scale)
        return min(min_x_scale, min_y_scale)
    
class TestApp(App):
    def build(self):
        root = Builder.load_string(kv)
        return root
    
TestApp().run()
