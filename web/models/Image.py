from Card import Card
class Image(Card):
    def __init__(self, img_path):
        self.img_path = img_path
        self.eclipse = "default"
        self.frame_width = "default"
    def set_img(self, eclipse, frame_width):
        self.eclipse = eclipse
        self.frame_width = frame_width

    def change_img(self, img_path):
        self.img_path = img_path

