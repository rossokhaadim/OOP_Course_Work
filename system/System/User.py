from SystemManage import SystemManage
from SystemManage import system_manage
from Company import Company


class User(SystemManage):
    def __init__(self):
        self.username = ""
        self.password = ""
        self.userData = {"companies": {}}
        self.user_companies = []
        self.accessed_buildings = []
        self.accessed_floors = []
        self.accessed_offices = []

    def add_company_to_user(self, company_name):
        answer = "THE COMPANY IS ADDED SUCCESSFULLY"
        already_exist = False
        added = False
        for key_company in self.userData["companies"].keys():
            if key_company == company_name:
                answer = "THE COMPANY IS ALREADY EXISTS IN THIS USER SYSTEM"
                already_exist = True
        if not already_exist:
            for company in system_manage.companies:
                if company.name == company_name:
                    # self.user_companies.append(company)
                    self.userData["companies"].update({company_name: {"buildings": {}}})
                    added = True
            if not added:
                answer = "ERROR. THE COMPANY DOES NOT EXIST"

    def add_building_to_user(self, building_address, company_name):
        answer = "THE BUILDING IS ADDED SUCCESSFULLY"
        already_exist = False
        added = False
        for building_key in self.userData["companies"][company_name]["buildings"].keys():
            if building_key == building_address:
                answer = "ERROR. THE BUILDING ALREADY EXISTS IN THIS USER SYSTEM"
                already_exist = True
        for company in self.userData["companies"].keys():
            for building in company["buildings"].keys():
                if building == building_address:
                    # self.accessed_buildings.append(building)
                    # comp = company.company_name
                    self.userData["companies"][company_name]["buildings"].update({building.address: {"floors": {}}})
                    added = True
        if not added:
            answer = "ERROR. THE COMPANY DOES NOT HAVE THIS BUILDING"


    def add_floor_to_user(self, building, floor_number, company):
        answer = "THE FLOOR IS ADDED SUCCESSFULLY"
        already_exist = False
        added = False
        for floor in self.userData["companies"][company]["buildings"][building]["floors"].keys():
            if floor_number == floor:
                answer = "ERROR. THE FLOOR ALREADY EXISTS IN THIS USER SYSTEM"
        # for floor in system_manage.companies.company.buildings.building.
    def add_office_to_user(self, company, building, floor, office):
        answer = "THE OFFICE IS ADDED SUCCESSFULLY"
        already_exist = False
        added = False

