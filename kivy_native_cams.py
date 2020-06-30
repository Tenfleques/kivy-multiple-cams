from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time
Builder.load_string('''
<MultipleCameras>:
    orientation: 'horizontal'
    CameraClick:
        id: first
        index: 0
    CameraClick:
        id: second
        index: 0
    CameraClick:
        id: third
        index: 0

<CameraClick>:
    orientation: 'vertical'
    index: -1
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
        index: root.index
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')


class CameraClick(BoxLayout):
            
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")

class MultipleCameras(BoxLayout):
    def build(self):
        pass

class TestCamera(App):

    def build(self):
        return MultipleCameras()


TestCamera().run()




