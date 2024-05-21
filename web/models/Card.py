class Card:
    def __init__(self):
        self.id = int()
        self.company_name = ""
        self.__key = ""
        self.img_path = ""

    def get_company_name(self):
        return self.company_name

    def get_key(self):
        return self.__key

    def get_img_path(self):
        return self.img_path

    def input_company_name(self, company_name):
        self.company_name = company_name

    def input_key(self, key):
        self.__key = key

    def input_img_path(self, img_path):
        self.img_path = img_path

