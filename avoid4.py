#!/usr/bin/env python3

"""
Simple test of the libavoid library from the Adaptagrams project.
This version uses poly-line othogonal routes for the connections attached to 
blocks.
"""

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty
from kivy.app import App
from kivy.lang import Builder

import adaptagrams as avoid

buffer_distance = 5.0

class Router(avoid.Router):
    def __init__(self, *args, **kw):
        self.connections = []
        super().__init__(*args, **kw)
        self.setRoutingParameter(avoid.shapeBufferDistance, buffer_distance)
        self.setRoutingParameter(avoid.crossingPenalty, 50000000)
        
    def processTransaction(self):
        super().processTransaction()
        for conn in self.connections:
            if conn.avoid_conn is not None and conn.avoid_conn.needsRepaint():
                conn.update_points()
                
router = Router(avoid.OrthogonalRouting)

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
    Block:
        id: block1
        pos: 100, 100
    Block:
        pos: 200, 100
    Block:
        pos: 300, 100
    Block:
        pos: 400, 100
    Block:
        id: block2
        pos: 500, 100
    Block:
        id: block3
        pos: 100, 200
    Block:
        pos: 200, 200
    Block:
        pos: 300, 200
    Block:
        pos: 400, 200
    Block:
        id: block4
        pos: 500, 200
    Block:
        id: block5
        pos: 100, 300
    Block:
        pos: 200, 300
    Block:
        pos: 300, 300
    Block:
        pos: 400, 300
    Block:
        id: block6
        pos: 500, 300
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

class Block(DragRect):
    def __init__(self, *args, **kw):
        self.avoid_shape = None
        super().__init__(*args, **kw)
        
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
    source = ObjectProperty(None)
    dest = ObjectProperty(None)
    
    def __init__(self, *args, **kw):
        self.avoid_conn = avoid.ConnRef(router)
        super().__init__(*args, **kw)
        router.connections.append(self)
        
    def on_source(self, *args, **kw):
        if self.source is not None:
            pin = avoid.ShapeConnectionPin(
                self.source.avoid_shape, 1, avoid.ATTACH_POS_RIGHT,
                avoid.ATTACH_POS_CENTRE, True, buffer_distance,
                avoid.ConnDirRight)
            src = avoid.ConnEnd(self.source.avoid_shape, 1)
            self.avoid_conn.setSourceEndpoint(src)
        self.update_avoid()
        
    def on_dest(self, *args, **kw):
        if self.dest is not None:
            pin = avoid.ShapeConnectionPin(
                self.dest.avoid_shape, 1, avoid.ATTACH_POS_LEFT,
                avoid.ATTACH_POS_CENTRE, True, buffer_distance,
                avoid.ConnDirLeft)
            dest = avoid.ConnEnd(self.dest.avoid_shape, 1)
            self.avoid_conn.setDestEndpoint(dest)
        self.update_avoid()
        
    def update_avoid(self, *args, **kw):
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

def connect(block1, block2):
    c = Connection()
    c.source = block1
    c.dest   = block2
    block1.update_avoid()
    block2.update_avoid()
    return c

class TestApp(App):
    def build(self):
        root = Builder.load_string(kv)
        root.add_widget(connect(root.ids.block1, root.ids.block2))
        root.add_widget(connect(root.ids.block4, root.ids.block3))
        root.add_widget(connect(root.ids.block5, root.ids.block6))
        return root
    
TestApp().run()
