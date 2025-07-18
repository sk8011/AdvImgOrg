from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.properties import ObjectProperty
import pickle
import os
from fpdf import FPDF

# App Window attributes
Config.set("graphics", 'width', '400')
Config.set("graphics", 'height', '600')

# Intro screen
class Intro(Screen):
    pass

# Folder creation screen
class FolderMaker(Screen):
    txt = ObjectProperty(None)
    
    # Code for the creation of folder/album
    def gen_folder(self):
        global folder_name, folder_path
        folder_name = self.txt.text
        folder_path = main_app_folder + folder_name + '/'
        os.mkdir(folder_path)
        print("Folder named", folder_name, 'is generated with the required metadata file.')
    pass

# Camera screen
class Cam(Screen):
    photo_name = ObjectProperty(None)
    
    # Code to capture and save photos
    def capture(self):
        global i_cam, d_cam
        img_name = self.photo_name.text
        camera = self.ids['camera']
        camera.export_to_png(folder_path + img_name + '.png')
        i_cam += 1
        d_cam[img_name] = i_cam
        print("Captured")
        self.photo_name.text = ""
    
    # Code for updating the metadata file
    def save(self):
        global i_cam, d_cam
        md_file_temp = open(folder_path + folder_name + '.dt', 'wb')
        pickle.dump(d_cam, md_file_temp)
        md_file_temp.close()
        d_cam = {}
        i_cam = 0
    pass

class Confirmview(Screen):
    def img_list_gen(self):
        global md_list
        filepath = folder_path + folder_name + '.dt'
        file_temp = open(filepath, 'rb')
        md_dict = pickle.load(file_temp)
        file_temp.close()
        md_list = list(md_dict.keys())
    pass

# Image viewing screen
class View(Screen):
    img = ObjectProperty(None)
    btn = ObjectProperty(None)
    
    def change(self):
        global p_view
        if p_view < len(md_list) - 1:
            p_view += 1
            self.img.source = folder_path + md_list[p_view] + '.png'
        else:
            self.manager.current = "pdf"
    pass

# PDF generator screen
class Pdfmaker(Screen):
    def pdfgen(self):
        pdf = FPDF()
        img = [folder_path + img + '.png' for img in md_list]
        for image in img:
            pdf.add_page()
            pdf.image(image)
        pdf.output(folder_path + folder_name + '.pdf', "F")
        print("Exported to", folder_path + folder_name, 'as', folder_name + '.pdf.')
    pass

# About screen
class About(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class advanced_image_organizer(App):
    def build(self):
        return Builder.load_string(kv)

kv = '''
WindowManager:
    Intro:
    FolderMaker:
    Cam:
    Confirmview:
    View:
    Pdfmaker:
    About:

<Intro>:
    name: "intro"
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Welcome to Advanced Image Organizer"
        Button:
            text: "Start"
            on_release:
                app.root.current = "foldermaker"

<FolderMaker>:
    name: "foldermaker"
    txt: txt
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: txt
            hint_text: "Enter folder name"
        Button:
            text: "Create Folder"
            on_release:
                root.gen_folder()
                app.root.current = "cam"
                
<Cam>:
    name: "cam"
    photo_name: photo_name
    BoxLayout:
        orientation: 'vertical'
        Camera:
            id: camera
            resolution: (640, 480)
            play: True
        TextInput:
            id: photo_name
            hint_text: "Enter photo name"
        Button:
            text: "Capture"
            on_release: root.capture()
        Button:
            text: "Save"
            on_release: root.save()
            app.root.current = "confirmview"

<Confirmview>:
    name: "confirmview"
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: "Generate Image List"
            on_release: root.img_list_gen()
        Button:
            text: "View Images"
            on_release: app.root.current = "view"

<View>:
    name: "view"
    img: img
    BoxLayout:
        orientation: 'vertical'
        Image:
            id: img
        Button:
            text: "Next Image"
            on_release: root.change()

<Pdfmaker>:
    name: "pdf"
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: "Generate PDF"
            on_release: root.pdfgen()
        Button:
            text: "Finish"
            on_release: app.root.current = "intro"

<About>:
    name: "about"
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Advanced Image Organizer App"
'''

if __name__ == '__main__':
    # Important variables
    folder_name = ""
    i_cam = 0
    d_cam = {}
    md_list = []
    p_view = -1
    main_app_folder = 'F:\Downloads\advanced_image_organizer_app\advanced_image_organizer_app'

    advanced_image_organizer().run()
