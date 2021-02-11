from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.relativelayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.config import Config
import os

from util.image_util import load_image
from util.model_util import predict


Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', '0')


class BaseWidget(Widget):
    pass


class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        color = (255, 255, 255, 100)
        with self.canvas:
            Color(*color)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=6)

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class MyPaintApp(App):

    def build(self):
        self.parent = BaseWidget()
        self.painter = MyPaintWidget()
        self.parent.add_widget(self.painter)
        return self.parent

    def clear_canvas(self):
        self.painter.canvas.clear()
        self.parent.ids.output_label.text = "Output: "

    def submit(self):
        image_path = os.path.join(os.getcwd(), 'image.png')
        self.parent.export_to_png(image_path)
        image_input = load_image(image_path)

        prediction = predict(image_input)

        self.parent.ids.output_label.text = "Output: " + str(prediction)

        is_training = open('../model/savings/training').readline() == 'True'
        if is_training:
            print(prediction)
            show_pop()

    def correct_digit_submit(self, text):
        if str(text).isdigit() and 0 <= int(text) <= 9:
            # TODO: automatic path, write in train image/label folders
            self.parent.export_to_png(os.path.join(os.getcwd(), ''))


class P(FloatLayout):
    pass


def show_pop():
    show = P()
    popup_window = Popup(title="Correct Input", content=show, size_hint=(None, None), size=(300, 300))
    popup_window.open()
