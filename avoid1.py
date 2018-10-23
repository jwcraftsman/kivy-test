#!/usr/bin/env python3

"""
Simple test of the libavoid library from the Adaptagrams project.
"""

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.app import App
from kivy.lang import Builder

import adaptagrams as avoid

class Router(avoid.Router):
    def __init__(self, *args, **kw):
        self.connections = []
        super().__init__(*args, **kw)
        
    def processTransaction(self):
        super().processTransaction()
        for conn in self.connections:
            if conn.avoid_conn is not None and conn.avoid_conn.needsRepaint():
                conn.update_points()
                
router = Router(avoid.PolyLineRouting)

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

<Connection>:
    canvas:
        Color:
            rgba: 1,0,0,.5
        Line:
            width: 1.1
            points: self._kvpoints

FloatLayout:
    DragRect:
        pos: 100, 100
    DragRect:
        pos: 200, 100
    DragRect:
        pos: 300, 100
    DragRect:
        pos: 400, 100
    DragRect:
        pos: 500, 100
    Connection:
        source: 25, 125
        dest: 625, 125
"""

# Similar to DragBehavior
class DragRect(FloatLayout):
    def __init__(self, *args, **kw):
        self.avoid_shape = None
        super().__init__(*args, **kw)
        
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

    def on_pos(self, *args, **kw):
        self.update_avoid()
        
    def update_avoid(self, *args, **kw):
        rectangle = avoid.AvoidRectangle(
            avoid.Point(self.x, self.y),
            avoid.Point(self.x + self.width,
                        self.y + self.height))
        if self.avoid_shape is None:
            self.avoid_shape = avoid.ShapeRef(router, rectangle)
        else:
            router.moveShape(self.avoid_shape, rectangle)
        router.processTransaction()
        
class Connection(Widget):
    _kvpoints= ListProperty((0, 0, 1, 1))
    source = ListProperty((0, 0))
    dest = ListProperty((1, 1))
    
    def __init__(self, *args, **kw):
        self.avoid_conn = None
        super().__init__(*args, **kw)
        router.connections.append(self)
        
    def on_source(self, *args, **kw):
        self.update_avoid()
        
    def on_dest(self, *args, **kw):
        self.update_avoid()
        
    def update_avoid(self, *args, **kw):
        src = avoid.ConnEnd(avoid.Point(self.source[0], self.source[1]))
        dest = avoid.ConnEnd(avoid.Point(self.dest[0], self.dest[1]))
        if self.avoid_conn is None:
            self.avoid_conn = avoid.ConnRef(router, src, dest)
        else:
            self.avoid_conn.setEndpoints(src, dest)
        router.processTransaction()
        
    def update_points(self, *args, **kw):
        if self.avoid_conn is not None:
            route = self.avoid_conn.displayRoute()
            points = []
            for i in range(0, route.size()):
                point = route.at(i)
                points.append(point.x)
                points.append(point.y)
            self._kvpoints = points

class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

TestApp().run()
