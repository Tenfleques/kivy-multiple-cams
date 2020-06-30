from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import time
import cv2 


Builder.load_string('''
<MultipleCameras>:
    orientation: 'horizontal'
    CameraClick:
        id: cam0
        index: 0
    CameraClick:
        id: cam1
        index: 0
    CameraClick:
        id: cam2
        index: 0

<CameraClick>:
    orientation: 'vertical'
    index: 0
    Image:
        id: camera
        size_hint_y: 1
    ToggleButton:
        text: 'Play'
        on_press: root.is_playing = not root.is_playing
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')


class CameraClick(BoxLayout):
    is_playing = False
    video_cap = None
    video_interval = None

    def build(self):
        pass

    def on_stop(self):
        self.stop_interval()

    def start_interval(self):
        self.video_cap = cv2.VideoCapture(self.index)
        fps = self.video_cap.get(cv2.CAP_PROP_FPS)
        interval = max(fps, 5)/1000
        self.update_image(None)
        self.video_interval = Clock.schedule_interval(self.update_image, interval)

    def stop_interval(self):
        if self.video_interval is not None:
            self.video_interval.cancel()
        
        if self.video_cap is not None:
            self.video_cap.release()

    def update_image(self, dt):
        if not self.is_playing:
            return 0

        if self.video_cap is None:
            self.stop_interval()
            return 0
        
        ret, frame = self.video_cap.read()
        if not ret:
            self.stop_interval()
            return 0

        frame = cv2.flip(frame, 0)

        buf = frame.tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.ids['camera'].texture = texture

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
    def start_all(self):
        ids = ["cam0", "cam1", "cam2"]
        for cam in ids:
            self.ids[cam].start_interval()


class TestCamera(App):

    def build(self):
        mcs = MultipleCameras()
        mcs.start_all()
        return mcs


TestCamera().run()




