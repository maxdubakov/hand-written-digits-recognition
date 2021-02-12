from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.relativelayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.config import Config
import os
from pathlib import Path

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
        is_training = open('../model/savings/training').readline() == 'True'
        if is_training:
            self.popup = show_pop()
        else:
            self.predict()

    def predict(self):
        image_path = os.path.join(os.getcwd(), 'image.png')
        self.parent.export_to_png(image_path)
        image_input = load_image(image_path)

        prediction = predict(image_input)

        self.parent.ids.output_label.text = "Output: " + str(prediction)
        print(prediction)

    def correct_digit_submit(self, text):
        self.popup.dismiss()
        if str(text).isdigit() and 0 <= int(text) <= 9:
            image_path = Path(os.getcwd()).parent.joinpath('new_images')
            self.parent.export_to_png(os.path.join(image_path, 'tmp.png'))
            image = load_image(os.path.join(image_path, 'tmp.png'))
            with open(os.path.join(image_path, 'train_images.csv'), 'a') as f:
                f.write(arr_to_string(image) + '\n')

            label = int(text)
            label_path = Path(os.getcwd()).parent.joinpath('new_labels')
            with open(os.path.join(label_path, 'train_labels.csv'), 'a') as f:
                f.write(str(label) + '\n')


class P(FloatLayout):
    pass


def show_pop():
    show = P()
    popup_window = Popup(title="Correct Input", content=show, size_hint=(None, None), size=(300, 300))
    popup_window.open()
    return popup_window


def arr_to_string(arr):
    return str([str(d) for d in arr])
