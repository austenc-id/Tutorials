from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from random import random

class PaintWidget(Widget):
    # react to user input on click
    def on_touch_down(self, touch):
        # sets a random color
        color = (random(), 1, 1)
        # changes canvas and allows it to be cleared
        with self.canvas:
            Color(*color, mode='hsv')
            # sets the diameter and shape of the user input
            d = 10.
            Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d,d))
            # defines the line when on_touch_move is called
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    # allows continuous drawing while clicked
    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]
class PaintApp(App):

    def build(self):
        # defines a canvas clear button
        parent = Widget()
        self.painter = PaintWidget()
        clear_button = Button(text='Clear')
        clear_button.bind(on_release=self.clear_canvas)
        parent.add_widget(self.painter)
        parent.add_widget(clear_button)
        return parent

    # clears the canvas
    def clear_canvas(self, obj):
        self.painter.canvas.clear()

if __name__ == '__main__':
    PaintApp().run()